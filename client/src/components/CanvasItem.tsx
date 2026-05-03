"use client";

import React, { useRef, useCallback, useEffect } from "react";
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
const HANDLE_BG = "#ffffff";
const ITEM_DEFAULT_COLOR = "#374151";
const ITEM_SELECTED_COLOR = "#1d4ed8";

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
  } = useCanvasStore();
  const isSelected = selectedId === item.instanceId;

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

  const onMouseDownItem = (e: React.MouseEvent) => {
    if ((e.target as Element).classList.contains("resize-handle")) return;
    e.stopPropagation();
    selectItem(item.instanceId);
    dragging.current = true;
    const pt = toCanvas(e.clientX, e.clientY);
    dragStart.current = { mx: pt.x, my: pt.y, ix: item.x, iy: item.y };
  };

  const onMouseDownHandle = (e: React.MouseEvent, corner: string) => {
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

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!isSelected) return;
      if (e.key === "Delete" || e.key === "Backspace")
        deleteItem(item.instanceId);
      if (e.key === "r" || e.key === "R")
        rotateItem(item.instanceId, (item.rotation + 90) % 360);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isSelected, item, deleteItem, rotateItem]);

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

  return (
    <g
      transform={`translate(${item.x}, ${item.y}) rotate(${item.rotation}, ${item.width / 2}, ${item.height / 2})`}
      onMouseDown={onMouseDownItem}
      style={{ cursor: dragging.current ? "grabbing" : "grab" }}
    >
      {isSelected && (
        <rect
          x={-2}
          y={-2}
          width={item.width + 4}
          height={item.height + 4}
          fill={ACCENT_FILL}
          stroke={ACCENT}
          strokeWidth={1.5 / zoom}
          strokeDasharray={`${4 / zoom} ${3 / zoom}`}
          rx={2}
        />
      )}

      {/* Render based on kind */}
      {item.kind === "image" && item.dataUrl ? (
        <>
          <image
            href={item.dataUrl}
            x={0}
            y={0}
            width={item.width}
            height={item.height}
            preserveAspectRatio="xMidYMid slice"
            style={{ pointerEvents: "none" }}
          />
          {/* subtle border for image items */}
          <rect
            x={0}
            y={0}
            width={item.width}
            height={item.height}
            fill="none"
            stroke={isSelected ? ACCENT : "#cec8be"}
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
              color: isSelected ? ITEM_SELECTED_COLOR : ITEM_DEFAULT_COLOR,
              pointerEvents: "none",
              userSelect: "none",
            }}
            dangerouslySetInnerHTML={{ __html: item.svg ?? "" }}
          />
        </foreignObject>
      )}

      {isSelected && (
        <text
          x={item.width / 2}
          y={-8 / zoom}
          textAnchor="middle"
          fill={ACCENT}
          fontSize={10 / zoom}
          fontFamily="'DM Mono', monospace"
          letterSpacing={0.5}
        >
          {item.label}
        </text>
      )}

      {isSelected &&
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
    </g>
  );
}
