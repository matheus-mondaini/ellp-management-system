import { NextResponse } from "next/server";

import { createMockOficina, listMockOficinas } from "../_state";

export function GET() {
  return NextResponse.json(listMockOficinas());
}

export async function POST(request: Request) {
  const payload = await request.json().catch(() => null);
  if (!payload) {
    return NextResponse.json({ detail: "Payload inválido" }, { status: 400 });
  }

  const created = createMockOficina(payload);
  return NextResponse.json(created, { status: 201 });
}
