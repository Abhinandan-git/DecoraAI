import { NextResponse } from "next/server";
import { CatalogItem } from "@/lib/catalog";

const BACKEND = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND}/api/catalogue`, {
      next: { revalidate: 60 }, // cache for 60 s in production
    });
    if (!res.ok) throw new Error(`Backend responded ${res.status}`);
    const data: CatalogItem[] = await res.json();
    return NextResponse.json(data);
  } catch {
    // Fallback: return empty array so the UI can still handle it gracefully
    return NextResponse.json(
      { error: "Could not reach backend" },
      { status: 502 },
    );
  }
}
