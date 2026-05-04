"""
services/image_service.py
--------------------------
LoRA-augmented Stable Diffusion image generation service.

Architecture
------------
- load_pipeline()    — called once at startup via lifespan
- unload_pipeline()  — called at shutdown to free GPU memory
- generate_image()   — public entry point used by the router

When MODEL_ENABLED=false (default for dev), or when diffusers/torch
are not installed, the service transparently returns a high-quality
parchment grid image so the frontend always gets a valid response.

Enabling your LoRA
------------------
1. pip install torch diffusers transformers accelerate safetensors
2. In .env set:
     MODEL_ENABLED=true
     SD_BASE_MODEL=runwayml/stable-diffusion-v1-5   # or your base model
     LORA_WEIGHTS_PATH=/absolute/path/to/lora        # dir OR .safetensors file
     LORA_SCALE=0.85
     DEVICE=auto
3. Restart the server — the pipeline loads once and stays in memory.
"""

import base64
import io
import logging
import random
import textwrap
from pathlib import Path
from typing import Optional

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Pipeline singleton ────────────────────────────────────────────────────────

_pipeline = None  # diffusers StableDiffusionPipeline instance
_pipeline_ready = False  # True only after a successful load


def _resolve_device() -> str:
    """Return the best available device, respecting the DEVICE config."""
    if settings.device != "auto":
        return settings.device
    try:
        import torch
        if torch.cuda.is_available():
            logger.info("Auto-detected device: cuda")
            return "cuda"
        if torch.backends.mps.is_available():
            logger.info("Auto-detected device: mps")
            return "mps"
    except ImportError:
        pass
    logger.info("Auto-detected device: cpu")
    return "cpu"


def load_pipeline() -> None:
    """
    Load the base SD model and fuse LoRA weights.
    Safe to call even when diffusers/torch are absent — logs a warning
    and leaves the service in fallback mode.
    """
    global _pipeline, _pipeline_ready

    if not settings.model_enabled:
        logger.info(
            "Diffusion model disabled (MODEL_ENABLED=false). "
            "Using parchment-grid fallback renderer."
        )
        return

    try:
        import torch
        from diffusers import StableDiffusionPipeline

        device = _resolve_device()
        dtype = torch.float16 if device in ("cuda", "mps") else torch.float32

        logger.info(
            "Loading base model '%s'  [device=%s  dtype=%s]",
            settings.sd_base_model, device, dtype,
        )

        pipe = StableDiffusionPipeline.from_pretrained(
            settings.sd_base_model,
            torch_dtype=dtype,
            safety_checker=None,  # floor-plan domain — no NSFW risk
            requires_safety_checker=False,
        )
        pipe = pipe.to(device)

        # ── Load LoRA weights ────────────────────────────────────────────────
        lora_path = Path(settings.lora_weights_path)

        if lora_path.exists():
            logger.info("Loading LoRA weights from: %s", lora_path)

            # diffusers ≥ 0.21 supports load_lora_weights for both dirs and
            # single .safetensors files.
            pipe.load_lora_weights(
                str(lora_path),
                adapter_name=settings.lora_adapter_name,
            )
            pipe.set_adapters(
                [settings.lora_adapter_name],
                adapter_weights=[settings.lora_scale],
            )
            logger.info(
                "LoRA adapter '%s' loaded at scale %.2f",
                settings.lora_adapter_name, settings.lora_scale,
            )
        else:
            logger.warning(
                "LoRA path not found: %s\n"
                "Running base model only. "
                "Update LORA_WEIGHTS_PATH in .env to point to your weights.",
                lora_path,
            )

        # ── Memory optimisations ─────────────────────────────────────────────
        if device == "cuda":
            try:
                pipe.enable_xformers_memory_efficient_attention()
                logger.info("xformers memory-efficient attention enabled.")
            except Exception:
                logger.debug("xformers not available — using standard attention.")
        pipe.enable_attention_slicing()

        _pipeline = pipe
        _pipeline_ready = True
        logger.info("Diffusion pipeline ready ✓")

    except ImportError as exc:
        logger.warning(
            "diffusers/torch not installed (%s). "
            "Run:  pip install torch diffusers transformers accelerate safetensors\n"
            "Or set MODEL_ENABLED=false to silence this warning. "
            "Using fallback renderer.",
            exc,
        )
    except Exception as exc:
        logger.error(
            "Pipeline load failed: %s — using fallback renderer.", exc, exc_info=True
        )


def unload_pipeline() -> None:
    """Release GPU memory gracefully on server shutdown."""
    global _pipeline, _pipeline_ready
    if _pipeline is not None:
        try:
            import torch
            del _pipeline
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass
        _pipeline = None
        _pipeline_ready = False
        logger.info("Diffusion pipeline unloaded.")


# ── Public API ────────────────────────────────────────────────────────────────

def generate_image(
        prompt: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        lora_scale: Optional[float] = None,
        seed: Optional[int] = None,
) -> dict:
    """
    Generate an image for *prompt*.

    Returns a dict that maps directly onto ImageResponse:
        { dataUrl, prompt, width, height, steps, seed, model }

    Per-request parameters override the .env defaults, making it easy
    for power users to experiment without restarting the server.
    """
    w = width or settings.image_width
    h = height or settings.image_height
    n = steps or settings.image_steps
    cfg = guidance_scale or settings.image_guidance_scale
    scale = lora_scale if lora_scale is not None else settings.lora_scale
    s = seed if seed is not None else random.randint(0, 2 ** 32 - 1)

    if _pipeline_ready and _pipeline is not None:
        return _run_pipeline(prompt, w, h, n, cfg, scale, s)
    return _render_fallback(prompt, w, h, n, s)


# ── Diffusion inference ───────────────────────────────────────────────────────

def _run_pipeline(
        prompt: str,
        width: int,
        height: int,
        steps: int,
        guidance_scale: float,
        lora_scale: float,
        seed: int,
) -> dict:
    import torch

    generator = torch.Generator(_pipeline.device).manual_seed(seed)

    # Allow callers to adjust the LoRA scale per-request without reloading
    try:
        _pipeline.set_adapters(
            [settings.lora_adapter_name],
            adapter_weights=[lora_scale],
        )
    except Exception:
        pass  # no LoRA loaded — silently continue

    result = _pipeline(
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )
    dataUrl = _pil_to_data_url(result.images[0])

    return {
        "dataUrl": dataUrl,
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed,
        "model": "lora",
    }


# ── Fallback renderer ─────────────────────────────────────────────────────────

def _render_fallback(
        prompt: str,
        width: int,
        height: int,
        steps: int,
        seed: int,
) -> dict:
    """Parchment dot-grid PNG with prompt overlaid — always available."""
    try:
        dataUrl = _render_with_pillow(prompt, width, height)
    except ImportError:
        dataUrl = _render_svg_fallback(prompt, width, height)

    return {
        "dataUrl": dataUrl,
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed,
        "model": "fallback",
    }


def _render_with_pillow(prompt: str, width: int, height: int) -> str:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (width, height), color=(247, 245, 240))
    draw = ImageDraw.Draw(img)

    # Major grid lines
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=(214, 207, 194), width=1)
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=(214, 207, 194), width=1)

    # Minor dot grid
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=(200, 191, 174))

    # Prompt label
    if prompt:
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15
            )
        except Exception:
            font = ImageFont.load_default()

        chars = max(1, (width - 48) // 9)
        lines = textwrap.wrap(prompt, width=chars)
        line_h = 21
        bh = len(lines) * line_h + 20
        bx, by = 24, (height - bh) // 2

        draw.rounded_rectangle(
            [bx - 12, by - 10, width - bx + 12, by + bh],
            radius=8, fill=(240, 237, 230), outline=(200, 191, 174), width=1,
        )
        for i, line in enumerate(lines):
            draw.text((bx, by + i * line_h + 4), line, fill=(120, 113, 108), font=font)

    return _pil_to_data_url(img)


def _render_svg_fallback(prompt: str, width: int, height: int) -> str:
    label = ""
    if prompt:
        esc = prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        label = (
            f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" '
            f'font-family="monospace" font-size="16" fill="#78716c">{esc}</text>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="#f7f5f0"/>'
        f'<defs><pattern id="d" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<circle cx="0" cy="0" r="1" fill="#c8bfae"/>'
        f'</pattern></defs>'
        f'<rect width="100%" height="100%" fill="url(#d)"/>'
        f'{label}'
        f'</svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def _pil_to_data_url(img) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()
