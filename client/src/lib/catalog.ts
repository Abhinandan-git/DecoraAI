export interface CatalogItem {
  id: string;
  label: string;
  category: "walls" | "openings" | "furniture" | "fixtures";
  defaultWidth: number;
  defaultHeight: number;
  svg: string;
}

export const CATEGORIES = [
  { id: "walls", label: "Walls" },
  { id: "openings", label: "Openings" },
  { id: "furniture", label: "Furniture" },
  { id: "fixtures", label: "Fixtures" },
] as const;

export type CategoryId = (typeof CATEGORIES)[number]["id"];
