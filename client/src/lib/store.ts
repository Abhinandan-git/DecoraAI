import { create } from "zustand";
import { CatalogItem } from "./catalog";

// ── Item types ────────────────────────────────────────────────────────────────

export type PlacedItemKind = "svg" | "image";

export interface PlacedItem {
  instanceId: string;
  kind: PlacedItemKind;
  catalogId: string;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
  // svg items
  svg?: string;
  // image items
  dataUrl?: string;
  label: string;
}

interface CanvasStore {
  items: PlacedItem[];
  selectedId: string | null;

  addItem: (catalogItem: CatalogItem, x: number, y: number) => void;
  addImageItem: (dataUrl: string, label: string, x: number, y: number) => void;
  moveItem: (instanceId: string, x: number, y: number) => void;
  resizeItem: (instanceId: string, width: number, height: number) => void;
  rotateItem: (instanceId: string, rotation: number) => void;
  deleteItem: (instanceId: string) => void;
  selectItem: (instanceId: string | null) => void;
  clearCanvas: () => void;
}

let counter = 0;

export const useCanvasStore = create<CanvasStore>((set) => ({
  items: [],
  selectedId: null,

  addItem: (catalogItem, x, y) => {
    const instanceId = `${catalogItem.id}-${++counter}`;
    set((state) => ({
      items: [
        ...state.items,
        {
          instanceId,
          kind: "svg",
          catalogId: catalogItem.id,
          x,
          y,
          width: catalogItem.defaultWidth,
          height: catalogItem.defaultHeight,
          rotation: 0,
          svg: catalogItem.svg,
          label: catalogItem.label,
        },
      ],
      selectedId: instanceId,
    }));
  },

  addImageItem: (dataUrl, label, x, y) => {
    const instanceId = `img-${++counter}`;
    set((state) => ({
      items: [
        ...state.items,
        {
          instanceId,
          kind: "image",
          catalogId: instanceId,
          x,
          y,
          width: 240,
          height: 160,
          rotation: 0,
          dataUrl,
          label,
        },
      ],
      selectedId: instanceId,
    }));
  },

  moveItem: (instanceId, x, y) => {
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId ? { ...item, x, y } : item,
      ),
    }));
  },

  resizeItem: (instanceId, width, height) => {
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId
          ? {
              ...item,
              width: Math.max(20, width),
              height: Math.max(20, height),
            }
          : item,
      ),
    }));
  },

  rotateItem: (instanceId, rotation) => {
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId ? { ...item, rotation } : item,
      ),
    }));
  },

  deleteItem: (instanceId) => {
    set((state) => ({
      items: state.items.filter((item) => item.instanceId !== instanceId),
      selectedId: state.selectedId === instanceId ? null : state.selectedId,
    }));
  },

  selectItem: (instanceId) => {
    set({ selectedId: instanceId });
  },

  clearCanvas: () => {
    set({ items: [], selectedId: null });
  },
}));
