"use client";

import React, { useCallback, useEffect, useRef } from "react";
import { PlacedItem, useCanvasStore } from "@/lib/store";

interface Props {
  item: PlacedItem;
  canvasRef: React.RefObject<SVGSVGElement | null>;
  zoom: number;
  panX: number;
  panY: number;
}

const HANDLE_SIZE = 8;
const ACCENT = "#2563eb";
const ACCENT_FILL = "rgba(37,99,235,0.07)";
const LOCKED_STROKE = "#f59e0b"; // amber — locked border
const LOCKED_FILL = "rgba(245,158,11,0.06)";
const HANDLE_BG = "#ffffff";
const ITEM_COLOR = "#374151";
const ITEM_SELECTED = "#1d4ed8";

export default function CanvasItem({
  item,
  canvasRef,
  zoom,
  panX,
  panY,
}: Props) {
  const {
    selectedId,
    selectItem,
    moveItem,
    resizeItem,
    deleteItem,
    rotateItem,
    toggleLock,
  } = useCanvasStore();

  const isSelected = selectedId === item.instanceId;
  const isLocked = item.locked;

  const dragging = useRef(false);
  const resizing = useRef<string | null>(null);
  const dragStart = useRef({ mx: 0, my: 0, ix: 0, iy: 0 });
  const resizeStart = useRef({ mx: 0, my: 0, w: 0, h: 0, x: 0, y: 0 });

  const toCanvas = useCallback(
    (clientX: number, clientY: number) => {
      const svg = canvasRef.current;
      if (!svg) return { x: 0, y: 0 };
      const rect = svg.getBoundingClientRect();
      return {
        x: (clientX - rect.left - panX) / zoom,
        y: (clientY - rect.top - panY) / zoom,
      };
    },
    [canvasRef, zoom, panX, panY],
  );

  // ── Mouse interactions ────────────────────────────────────────────────────

  const onMouseDownItem = (e: React.MouseEvent) => {
    if ((e.target as Element).classList.contains("resize-handle")) return;
    e.stopPropagation();
    selectItem(item.instanceId);
    // Only start dragging if unlocked
    if (!isLocked) {
      dragging.current = true;
      const pt = toCanvas(e.clientX, e.clientY);
      dragStart.current = { mx: pt.x, my: pt.y, ix: item.x, iy: item.y };
    }
  };

  const onMouseDownHandle = (e: React.MouseEvent, corner: string) => {
    if (isLocked) return;
    e.stopPropagation();
    e.preventDefault();
    resizing.current = corner;
    const pt = toCanvas(e.clientX, e.clientY);
    resizeStart.current = {
      mx: pt.x,
      my: pt.y,
      w: item.width,
      h: item.height,
      x: item.x,
      y: item.y,
    };
  };

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      const pt = toCanvas(e.clientX, e.clientY);
      if (dragging.current) {
        const dx = pt.x - dragStart.current.mx;
        const dy = pt.y - dragStart.current.my;
        moveItem(
          item.instanceId,
          dragStart.current.ix + dx,
          dragStart.current.iy + dy,
        );
      } else if (resizing.current) {
        const dx = pt.x - resizeStart.current.mx;
        const dy = pt.y - resizeStart.current.my;
        const c = resizing.current;
        let nw = resizeStart.current.w;
        let nh = resizeStart.current.h;
        let nx = resizeStart.current.x;
        let ny = resizeStart.current.y;
        if (c.includes("e")) nw = resizeStart.current.w + dx;
        if (c.includes("s")) nh = resizeStart.current.h + dy;
        if (c.includes("w")) {
          nw = resizeStart.current.w - dx;
          nx = resizeStart.current.x + dx;
        }
        if (c.includes("n")) {
          nh = resizeStart.current.h - dy;
          ny = resizeStart.current.y + dy;
        }
        if (nw >= 20 && nh >= 20) {
          resizeItem(item.instanceId, nw, nh);
          if (c.includes("w") || c.includes("n"))
            moveItem(item.instanceId, nx, ny);
        }
      }
    };
    const onUp = () => {
      dragging.current = false;
      resizing.current = null;
    };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, [item, toCanvas, moveItem, resizeItem]);

  // ── Keyboard shortcuts ────────────────────────────────────────────────────

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!isSelected) return;
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if (e.key === "Delete" || e.key === "Backspace")
        deleteItem(item.instanceId);
      if (!isLocked) {
        if (e.key === "r" || e.key === "R")
          rotateItem(item.instanceId, (item.rotation + 90) % 360);
      }
      if (e.key === "l" || e.key === "L") toggleLock(item.instanceId);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isSelected, isLocked, item, deleteItem, rotateItem, toggleLock]);

  // ── Render helpers ────────────────────────────────────────────────────────

  const selectionStroke = isLocked ? LOCKED_STROKE : ACCENT;
  const selectionFill = isLocked ? LOCKED_FILL : ACCENT_FILL;

  const handles = [
    { id: "nw", cx: 0, cy: 0 },
    { id: "ne", cx: item.width, cy: 0 },
    { id: "se", cx: item.width, cy: item.height },
    { id: "sw", cx: 0, cy: item.height },
    { id: "n", cx: item.width / 2, cy: 0 },
    { id: "e", cx: item.width, cy: item.height / 2 },
    { id: "s", cx: item.width / 2, cy: item.height },
    { id: "w", cx: 0, cy: item.height / 2 },
  ];

  const cursorMap: Record<string, string> = {
    nw: "nw-resize",
    ne: "ne-resize",
    se: "se-resize",
    sw: "sw-resize",
    n: "n-resize",
    e: "e-resize",
    s: "s-resize",
    w: "w-resize",
  };

  // Lock badge icon path (simple padlock)
  const lockIconSize = 14 / zoom;
  const lockIconX = item.width - lockIconSize - 4 / zoom;
  const lockIconY = 4 / zoom;

  return (
    <g
      transform={`translate(${item.x}, ${item.y}) rotate(${item.rotation}, ${item.width / 2}, ${item.height / 2})`}
      onMouseDown={onMouseDownItem}
      style={{
        cursor: isLocked ? "pointer" : dragging.current ? "grabbing" : "grab",
      }}
    >
      {/* Selection / locked border */}
      {isSelected && (
        <rect
          x={-2}
          y={-2}
          width={item.width + 4}
          height={item.height + 4}
          fill={selectionFill}
          stroke={selectionStroke}
          strokeWidth={1.5 / zoom}
          strokeDasharray={
            isLocked ? `${6 / zoom} ${3 / zoom}` : `${4 / zoom} ${3 / zoom}`
          }
          rx={2}
        />
      )}

      {/* Content */}
      {item.kind === "image" && item.dataUrl ? (
        <>
          <image
            href={item.dataUrl}
            x={0}
            y={0}
            width={item.width}
            height={item.height}
            preserveAspectRatio="xMidYMid slice"
          />
          {/* Transparent hit area — ensures mousedown fires on the <g> in all browsers */}
          <rect
            x={0}
            y={0}
            width={item.width}
            height={item.height}
            fill="transparent"
            stroke={isSelected ? selectionStroke : "#cec8be"}
            strokeWidth={1 / zoom}
            rx={2}
          />
        </>
      ) : (
        <foreignObject x={0} y={0} width={item.width} height={item.height}>
          <div
            // @ts-expect-error xmlns for foreignObject
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              width: "100%",
              height: "100%",
              color: isSelected ? ITEM_SELECTED : ITEM_COLOR,
              pointerEvents: "none",
              userSelect: "none",
            }}
            dangerouslySetInnerHTML={{ __html: item.svg ?? "" }}
          />
        </foreignObject>
      )}

      {/* Label above when selected */}
      {isSelected && (
        <text
          x={item.width / 2}
          y={-8 / zoom}
          textAnchor="middle"
          fill={selectionStroke}
          fontSize={10 / zoom}
          fontFamily="'DM Mono', monospace"
          letterSpacing={0.5}
        >
          {item.label}
          {isLocked ? " 🔒" : ""}
        </text>
      )}

      {/* Lock badge — always visible on image items that are locked */}
      {isLocked && (
        <g transform={`translate(${lockIconX}, ${lockIconY})`}>
          <rect
            x={0}
            y={0}
            width={lockIconSize}
            height={lockIconSize}
            rx={lockIconSize * 0.25}
            fill={LOCKED_STROKE}
            opacity={0.9}
          />
          {/* Padlock shackle (top arc) */}
          <path
            d={`M ${lockIconSize * 0.28} ${lockIconSize * 0.45}
                L ${lockIconSize * 0.28} ${lockIconSize * 0.3}
                A ${lockIconSize * 0.22} ${lockIconSize * 0.22} 0 0 1 ${lockIconSize * 0.72} ${lockIconSize * 0.3}
                L ${lockIconSize * 0.72} ${lockIconSize * 0.45}`}
            fill="none"
            stroke="white"
            strokeWidth={lockIconSize * 0.14}
            strokeLinecap="round"
          />
          {/* Padlock body */}
          <rect
            x={lockIconSize * 0.18}
            y={lockIconSize * 0.44}
            width={lockIconSize * 0.64}
            height={lockIconSize * 0.42}
            rx={lockIconSize * 0.1}
            fill="white"
            opacity={0.9}
          />
          {/* Keyhole */}
          <circle
            cx={lockIconSize * 0.5}
            cy={lockIconSize * 0.62}
            r={lockIconSize * 0.1}
            fill={LOCKED_STROKE}
          />
          <rect
            x={lockIconSize * 0.46}
            y={lockIconSize * 0.62}
            width={lockIconSize * 0.08}
            height={lockIconSize * 0.12}
            fill={LOCKED_STROKE}
          />
        </g>
      )}

      {/* Resize handles — only when selected and unlocked */}
      {isSelected &&
        !isLocked &&
        handles.map((h) => (
          <rect
            key={h.id}
            className="resize-handle"
            x={h.cx - HANDLE_SIZE / 2 / zoom}
            y={h.cy - HANDLE_SIZE / 2 / zoom}
            width={HANDLE_SIZE / zoom}
            height={HANDLE_SIZE / zoom}
            fill={HANDLE_BG}
            stroke={ACCENT}
            strokeWidth={1.5 / zoom}
            rx={1.5 / zoom}
            style={{ cursor: cursorMap[h.id] }}
            onMouseDown={(e) => onMouseDownHandle(e, h.id)}
          />
        ))}

      {/* Corner markers when selected + locked (show bounds, no interaction) */}
      {isSelected &&
        isLocked &&
        [
          { cx: 0, cy: 0 },
          { cx: item.width, cy: 0 },
          { cx: item.width, cy: item.height },
          { cx: 0, cy: item.height },
        ].map((h, i) => (
          <rect
            key={i}
            x={h.cx - HANDLE_SIZE / 2 / zoom}
            y={h.cy - HANDLE_SIZE / 2 / zoom}
            width={HANDLE_SIZE / zoom}
            height={HANDLE_SIZE / zoom}
            fill={LOCKED_STROKE}
            opacity={0.5}
            rx={1.5 / zoom}
          />
        ))}
    </g>
  );
}
