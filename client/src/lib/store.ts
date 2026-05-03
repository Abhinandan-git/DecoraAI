import { create } from "zustand";
import { CatalogItem } from "./catalog";

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
  svg?: string;
  dataUrl?: string;
  label: string;
  locked: boolean;
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
  toggleLock: (instanceId: string) => void;
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
          locked: false,
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
          locked: false,
        },
      ],
      selectedId: instanceId,
    }));
  },

  moveItem: (instanceId, x, y) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId && !item.locked
          ? { ...item, x, y }
          : item,
      ),
    })),

  resizeItem: (instanceId, width, height) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId && !item.locked
          ? {
              ...item,
              width: Math.max(20, width),
              height: Math.max(20, height),
            }
          : item,
      ),
    })),

  rotateItem: (instanceId, rotation) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId && !item.locked
          ? { ...item, rotation }
          : item,
      ),
    })),

  deleteItem: (instanceId) =>
    set((state) => ({
      items: state.items.filter((item) => item.instanceId !== instanceId),
      selectedId: state.selectedId === instanceId ? null : state.selectedId,
    })),

  selectItem: (instanceId) => set({ selectedId: instanceId }),

  toggleLock: (instanceId) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.instanceId === instanceId
          ? { ...item, locked: !item.locked }
          : item,
      ),
    })),

  clearCanvas: () => set({ items: [], selectedId: null }),
}));
