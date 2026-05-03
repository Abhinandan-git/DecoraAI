"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { useCanvasStore } from "@/lib/store";
import { useCatalogue } from "@/lib/api";
import CanvasItem from "./CanvasItem";
import { Minus, Plus, RotateCw, X } from "lucide-react";

const GRID = 20;
const MIN_ZOOM = 0.2;
const MAX_ZOOM = 3;

function snapToGrid(v: number) {
  return Math.round(v / GRID) * GRID;
}

export default function Canvas() {
  const svgRef = useRef<SVGSVGElement>(null);
  const {
    items,
    addItem,
    addImageItem,
    selectItem,
    selectedId,
    deleteItem,
    toggleLock,
  } = useCanvasStore();
  const { items: catalogItems } = useCatalogue();

  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 60, y: 60 });
  const panning = useRef(false);
  const lastPan = useRef({ x: 0, y: 0 });

  // ── Wheel zoom ──────────────────────────────────────────────────────────────
  const onWheel = useCallback((e: WheelEvent) => {
    e.preventDefault();
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const delta = e.deltaY < 0 ? 1.1 : 0.9;
    setZoom((z) => {
      const nz = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, z * delta));
      setPan((p) => ({
        x: mx - (mx - p.x) * (nz / z),
        y: my - (my - p.y) * (nz / z),
      }));
      return nz;
    });
  }, []);

  useEffect(() => {
    const el = svgRef.current;
    if (!el) return;
    el.addEventListener("wheel", onWheel, { passive: false });
    return () => el.removeEventListener("wheel", onWheel);
  }, [onWheel]);

  // ── Pan + click-away deselect ─────────────────────────────────────────────
  const onMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1) {
      panning.current = true;
      lastPan.current = { x: e.clientX, y: e.clientY };
      return;
    }
    if (e.button === 0) {
      const tag = (e.target as SVGElement).tagName;
      if (["svg", "rect", "image", "defs", "pattern"].includes(tag)) {
        selectItem(null);
        panning.current = true;
        lastPan.current = { x: e.clientX, y: e.clientY };
      }
    }
  };

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!panning.current) return;
      setPan((p) => ({
        x: p.x + e.clientX - lastPan.current.x,
        y: p.y + e.clientY - lastPan.current.y,
      }));
      lastPan.current = { x: e.clientX, y: e.clientY };
    };
    const onUp = () => {
      panning.current = false;
    };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, []);

  // ── Drop handler: SVG from toolbar OR image from chat ────────────────────
  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  };

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      if (!svgRef.current) return;
      const rect = svgRef.current.getBoundingClientRect();

      // Chat image drop
      const chatDataUrl = e.dataTransfer.getData("chatImageDataUrl");
      if (chatDataUrl) {
        const label = e.dataTransfer.getData("chatImageLabel") || "Image";
        const cx = snapToGrid((e.clientX - rect.left - pan.x) / zoom - 120);
        const cy = snapToGrid((e.clientY - rect.top - pan.y) / zoom - 80);
        addImageItem(chatDataUrl, label, cx, cy);
        return;
      }

      // Toolbar SVG drop
      const catalogId = e.dataTransfer.getData("catalogId");
      const item = catalogItems.find((c) => c.id === catalogId);
      if (!item) return;
      const cx = snapToGrid(
        (e.clientX - rect.left - pan.x) / zoom - item.defaultWidth / 2,
      );
      const cy = snapToGrid(
        (e.clientY - rect.top - pan.y) / zoom - item.defaultHeight / 2,
      );
      addItem(item, cx, cy);
    },
    [addItem, addImageItem, catalogItems, pan, zoom],
  );

  // ── Keyboard shortcuts ───────────────────────────────────────────────────
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;

      if ((e.key === "Delete" || e.key === "Backspace") && selectedId) {
        deleteItem(selectedId);
      }
      if (e.key === "Escape") selectItem(null);
      if ((e.key === "l" || e.key === "L") && selectedId)
        toggleLock(selectedId);
      if (e.key === "0" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        setZoom(1);
        setPan({ x: 60, y: 60 });
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selectedId, deleteItem, selectItem, toggleLock]);

  // ── Selected item info ───────────────────────────────────────────────────
  const selectedItem = items.find((i) => i.instanceId === selectedId);

  return (
    <div className="canvas-container">
      <svg
        ref={svgRef}
        className="canvas-svg"
        onMouseDown={onMouseDown}
        onDragOver={onDragOver}
        onDrop={onDrop}
      >
        <defs>
          <pattern
            id="grid-dots"
            x={pan.x % (GRID * zoom)}
            y={pan.y % (GRID * zoom)}
            width={GRID * zoom}
            height={GRID * zoom}
            patternUnits="userSpaceOnUse"
          >
            <circle cx={0} cy={0} r={0.9} fill="#bfb8ab" />
          </pattern>
          <pattern
            id="grid-major"
            x={pan.x % (GRID * 5 * zoom)}
            y={pan.y % (GRID * 5 * zoom)}
            width={GRID * 5 * zoom}
            height={GRID * 5 * zoom}
            patternUnits="userSpaceOnUse"
          >
            <path
              d={`M ${GRID * 5 * zoom} 0 L 0 0 0 ${GRID * 5 * zoom}`}
              fill="none"
              stroke="#d1cabc"
              strokeWidth="0.6"
            />
          </pattern>
        </defs>

        <rect width="100%" height="100%" fill="url(#grid-dots)" />
        <rect width="100%" height="100%" fill="url(#grid-major)" />

        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {items.map((item) => (
            <CanvasItem
              key={item.instanceId}
              item={item}
              canvasRef={svgRef}
              zoom={zoom}
              panX={pan.x}
              panY={pan.y}
            />
          ))}
        </g>
      </svg>

      {/* Zoom HUD */}
      <div className="canvas-hud">
        <button
          className="hud-btn"
          onClick={() => setZoom((z) => Math.min(MAX_ZOOM, z + 0.15))}
        >
          <Plus size={14} />
        </button>
        <button
          className="hud-btn"
          onClick={() => {
            setZoom(1);
            setPan({ x: 60, y: 60 });
          }}
        >
          {Math.round(zoom * 100)}%
        </button>
        <button
          className="hud-btn"
          onClick={() => setZoom((z) => Math.max(MIN_ZOOM, z - 0.15))}
        >
          <Minus size={14} />
        </button>
      </div>

      {/* Empty state hint */}
      {items.length === 0 && (
        <div className="canvas-hint">
          <span>Drag elements from the toolbar to begin</span>
        </div>
      )}

      {/* Selection context bar */}
      {selectedItem && (
        <div className="selection-bar">
          {/* Item name + lock status */}
          <span
            className={`selection-label ${selectedItem.locked ? "selection-label--locked" : ""}`}
          >
            {selectedItem.locked ? "🔒" : "◈"} {selectedItem.label}
          </span>

          {/* Only show rotate for unlocked items */}
          {!selectedItem.locked && (
            <button
              className="sel-btn"
              onClick={() =>
                useCanvasStore
                  .getState()
                  .rotateItem(
                    selectedItem.instanceId,
                    (selectedItem.rotation + 90) % 360,
                  )
              }
            >
              <RotateCw size={12} /> Rotate
            </button>
          )}

          {/* Lock / unlock — only for image items */}
          {selectedItem.kind === "image" && (
            <button
              className={`sel-btn ${selectedItem.locked ? "sel-btn--unlock" : "sel-btn--lock"}`}
              onClick={() => toggleLock(selectedItem.instanceId)}
            >
              {selectedItem.locked ? "🔓 Unlock" : "🔒 Lock"}
            </button>
          )}

          <button
            className="sel-btn sel-delete"
            onClick={() => deleteItem(selectedItem.instanceId)}
          >
            <X size={12} /> Delete
          </button>
        </div>
      )}
    </div>
  );
}
