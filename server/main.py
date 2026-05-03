"""
FastAPI backend for Blueprint Floor Plan Editor.

Endpoints:
  GET  /api/catalogue            → list of SVG floor plan elements
  GET  /api/background-image     → generated grid image (base64 PNG)
                                   ?prompt=<text>  optional label overlay
  POST /api/chat                 → { message } → { reply }

Run with:
  pip install fastapi uvicorn pillow
  uvicorn main:app --reload --port 8000
"""

import base64
import io
import textwrap
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

app = FastAPI(title="Blueprint API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Catalogue ─────────────────────────────────────────────────────────────────

CATALOGUE = [
    {"id":"wall-h","label":"Wall H","category":"walls","defaultWidth":120,"defaultHeight":12,"svg":'<svg viewBox="0 0 120 12" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="120" height="12" fill="currentColor"/></svg>'},
    {"id":"wall-v","label":"Wall V","category":"walls","defaultWidth":12,"defaultHeight":120,"svg":'<svg viewBox="0 0 12 120" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="12" height="120" fill="currentColor"/></svg>'},
    {"id":"wall-corner","label":"Corner","category":"walls","defaultWidth":72,"defaultHeight":72,"svg":'<svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="12" height="72" fill="currentColor"/><rect x="12" y="0" width="60" height="12" fill="currentColor"/></svg>'},
    {"id":"wall-t","label":"T-Wall","category":"walls","defaultWidth":72,"defaultHeight":72,"svg":'<svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="72" height="12" fill="currentColor"/><rect x="30" y="12" width="12" height="60" fill="currentColor"/></svg>'},
    {"id":"door-single","label":"Door","category":"openings","defaultWidth":80,"defaultHeight":80,"svg":'<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="8" height="80" fill="currentColor"/><rect x="8" y="72" width="72" height="8" fill="currentColor"/><path d="M8 0 L80 0" stroke="currentColor" stroke-width="8" fill="none"/><path d="M16 8 Q16 72 72 72" stroke="currentColor" stroke-width="1.5" fill="none" stroke-dasharray="4 3" opacity="0.5"/></svg>'},
    {"id":"door-double","label":"Double Door","category":"openings","defaultWidth":120,"defaultHeight":80,"svg":'<svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="8" height="80" fill="currentColor"/><rect x="112" y="0" width="8" height="80" fill="currentColor"/><rect x="8" y="72" width="104" height="8" fill="currentColor"/><path d="M8 0 L112 0" stroke="currentColor" stroke-width="8" fill="none"/><path d="M16 8 Q16 68 60 72" stroke="currentColor" stroke-width="1.5" fill="none" stroke-dasharray="4 3" opacity="0.5"/><path d="M104 8 Q104 68 60 72" stroke="currentColor" stroke-width="1.5" fill="none" stroke-dasharray="4 3" opacity="0.5"/></svg>'},
    {"id":"window","label":"Window","category":"openings","defaultWidth":80,"defaultHeight":16,"svg":'<svg viewBox="0 0 80 16" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="80" height="16" fill="currentColor" opacity="0.15"/><rect x="0" y="0" width="80" height="4" fill="currentColor"/><rect x="0" y="12" width="80" height="4" fill="currentColor"/><line x1="40" y1="0" x2="40" y2="16" stroke="currentColor" stroke-width="1.5"/></svg>'},
    {"id":"sliding-door","label":"Sliding","category":"openings","defaultWidth":80,"defaultHeight":16,"svg":'<svg viewBox="0 0 80 16" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="80" height="16" fill="currentColor" opacity="0.1"/><rect x="0" y="0" width="80" height="4" fill="currentColor"/><rect x="0" y="12" width="80" height="4" fill="currentColor"/><rect x="4" y="4" width="36" height="8" fill="currentColor" opacity="0.4" rx="1"/><rect x="40" y="4" width="36" height="8" fill="currentColor" opacity="0.25" rx="1"/></svg>'},
    {"id":"sofa","label":"Sofa","category":"furniture","defaultWidth":120,"defaultHeight":60,"svg":'<svg viewBox="0 0 120 60" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="10" width="120" height="50" rx="6" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="2"/><rect x="0" y="10" width="120" height="18" rx="6" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="0" y="10" width="16" height="50" rx="4" fill="currentColor" opacity="0.4" stroke="currentColor" stroke-width="1.5"/><rect x="104" y="10" width="16" height="50" rx="4" fill="currentColor" opacity="0.4" stroke="currentColor" stroke-width="1.5"/></svg>'},
    {"id":"bed-single","label":"Single Bed","category":"furniture","defaultWidth":80,"defaultHeight":120,"svg":'<svg viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="76" height="116" rx="4" fill="currentColor" opacity="0.12" stroke="currentColor" stroke-width="2"/><rect x="6" y="6" width="68" height="30" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="6" y="42" width="68" height="70" rx="2" fill="currentColor" opacity="0.18" stroke="currentColor" stroke-width="1"/></svg>'},
    {"id":"bed-double","label":"Double Bed","category":"furniture","defaultWidth":120,"defaultHeight":120,"svg":'<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="116" height="116" rx="4" fill="currentColor" opacity="0.12" stroke="currentColor" stroke-width="2"/><rect x="6" y="6" width="108" height="30" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="6" y="42" width="108" height="72" rx="2" fill="currentColor" opacity="0.18" stroke="currentColor" stroke-width="1"/></svg>'},
    {"id":"desk","label":"Desk","category":"furniture","defaultWidth":100,"defaultHeight":55,"svg":'<svg viewBox="0 0 100 55" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="96" height="51" rx="2" fill="currentColor" opacity="0.12" stroke="currentColor" stroke-width="2"/><rect x="2" y="2" width="96" height="10" rx="2" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/></svg>'},
    {"id":"dining-table","label":"Table","category":"furniture","defaultWidth":100,"defaultHeight":70,"svg":'<svg viewBox="0 0 100 70" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="10" width="80" height="50" rx="3" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="2"/><rect x="14" y="4" width="18" height="12" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="68" y="4" width="18" height="12" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="54" width="18" height="12" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/><rect x="68" y="54" width="18" height="12" rx="3" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1.5"/></svg>'},
    {"id":"toilet","label":"Toilet","category":"fixtures","defaultWidth":48,"defaultHeight":68,"svg":'<svg viewBox="0 0 48 68" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="0" width="36" height="20" rx="3" fill="currentColor" opacity="0.2" stroke="currentColor" stroke-width="1.5"/><ellipse cx="24" cy="48" rx="20" ry="18" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="2"/><ellipse cx="24" cy="48" rx="14" ry="13" fill="currentColor" opacity="0.08" stroke="currentColor" stroke-width="1"/></svg>'},
    {"id":"bathtub","label":"Bathtub","category":"fixtures","defaultWidth":70,"defaultHeight":130,"svg":'<svg viewBox="0 0 70 130" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="66" height="126" rx="10" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="2"/><rect x="8" y="8" width="54" height="114" rx="8" fill="currentColor" opacity="0.08" stroke="currentColor" stroke-width="1"/></svg>'},
    {"id":"sink","label":"Sink","category":"fixtures","defaultWidth":56,"defaultHeight":50,"svg":'<svg viewBox="0 0 56 50" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="52" height="46" rx="4" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="2"/><rect x="8" y="8" width="40" height="34" rx="8" fill="currentColor" opacity="0.08" stroke="currentColor" stroke-width="1"/></svg>'},
    {"id":"staircase","label":"Stairs","category":"fixtures","defaultWidth":80,"defaultHeight":120,"svg":'<svg viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="80" height="120" fill="currentColor" opacity="0.05" stroke="currentColor" stroke-width="2"/><line x1="0" y1="10" x2="80" y2="10" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="22" x2="80" y2="22" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="34" x2="80" y2="34" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="46" x2="80" y2="46" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="58" x2="80" y2="58" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="70" x2="80" y2="70" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="82" x2="80" y2="82" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="94" x2="80" y2="94" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="106" x2="80" y2="106" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><line x1="0" y1="118" x2="80" y2="118" stroke="currentColor" stroke-width="1.5" opacity="0.6"/><path d="M10 110 L70 10" stroke="currentColor" stroke-width="1.5" opacity="0.3" stroke-dasharray="3 3"/></svg>'},
]


@app.get("/api/catalogue")
def get_catalogue():
    return JSONResponse(content=CATALOGUE)


# ── Background / prompt image ─────────────────────────────────────────────────

def _generate_grid_image(width: int = 800, height: int = 560, prompt: Optional[str] = None) -> str:
    """
    Generates a parchment-grid PNG with an optional prompt label overlaid.
    Falls back to SVG if Pillow is unavailable.
    """
    if not PIL_AVAILABLE:
        label_el = ""
        if prompt:
            escaped = prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            label_el = f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="monospace" font-size="18" fill="#78716c" opacity="0.6">{escaped}</text>'
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="#f7f5f0"/>
  <defs>
    <pattern id="dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="0" cy="0" r="1" fill="#c8bfae" opacity="0.8"/>
    </pattern>
    <pattern id="major" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#d6cfc2" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#dots)"/>
  <rect width="100%" height="100%" fill="url(#major)"/>
  {label_el}
</svg>"""
        b64 = base64.b64encode(svg.encode()).decode()
        return f"data:image/svg+xml;base64,{b64}"

    img = Image.new("RGB", (width, height), color=(247, 245, 240))
    draw = ImageDraw.Draw(img)

    # Major grid lines
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=(214, 207, 194), width=1)
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=(214, 207, 194), width=1)

    # Minor dots
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=(200, 191, 174))

    # Prompt label overlay
    if prompt:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
        except Exception:
            font = ImageFont.load_default()

        # Wrap text to fit width
        chars_per_line = max(1, (width - 40) // 10)
        lines = textwrap.wrap(prompt, width=chars_per_line)
        line_h = 22
        block_h = len(lines) * line_h + 20
        block_y = (height - block_h) // 2
        block_x = 20

        # Background pill
        draw.rounded_rectangle(
            [block_x - 10, block_y - 8, width - block_x + 10, block_y + block_h],
            radius=8,
            fill=(240, 237, 230),
            outline=(200, 191, 174),
            width=1,
        )

        # Text lines
        for i, line in enumerate(lines):
            draw.text(
                (block_x, block_y + i * line_h + 4),
                line,
                fill=(120, 113, 108),
                font=font,
            )

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{b64}"


@app.get("/api/background-image")
def get_background_image(prompt: Optional[str] = Query(default=None)):
    data_url = _generate_grid_image(prompt=prompt)
    return JSONResponse(content={"dataUrl": data_url, "type": "grid"})


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
def post_chat(body: ChatRequest):
    """
    Stateless chat endpoint.  All conversation context is managed by the
    backend — plug in your LLM / RAG pipeline here.

    For now returns a helpful placeholder so the frontend is fully wired.
    Replace the logic inside this function with your actual chatbot call.
    """
    msg = body.message.strip()

    # ── Plug your chatbot here ────────────────────────────────────────────────
    # Example with OpenAI:
    #
    # import openai
    # client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # completion = client.chat.completions.create(
    #   model="gpt-4o",
    #   messages=[
    #       {"role": "system", "content": "You are a helpful floor plan assistant."},
    #       {"role": "user", "content": msg},
    #   ],
    # )
    # reply = completion.choices[0].message.content
    #
    # ─────────────────────────────────────────────────────────────────────────

    # Placeholder response
    reply = (
        f"I received: \"{msg}\"\n\n"
        "This is a placeholder — wire up your LLM in `backend/main.py` "
        "inside the `post_chat` function. Tip: type /image <description> "
        "to generate a reference image you can drag onto the canvas."
    )

    return JSONResponse(content={"reply": reply})
