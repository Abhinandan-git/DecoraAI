import { NextRequest, NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET(req: NextRequest) {
  try {
    const prompt = req.nextUrl.searchParams.get("prompt") ?? "";
    const url = prompt
      ? `${BACKEND}/api/background-image?prompt=${encodeURIComponent(prompt)}`
      : `${BACKEND}/api/background-image`;

    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`Backend responded ${res.status}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
