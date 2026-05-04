import { NextRequest, NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL ?? "http://localhost:8000";

// GET — canvas background, no auth needed
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

// POST — /image chat command, forwards JWT + session_id so image is saved to history
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const token = req.cookies.get("bp_token")?.value ?? "";

    const res = await fetch(`${BACKEND}/api/background-image`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    if (!res.ok) throw new Error(`Backend responded ${res.status}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
