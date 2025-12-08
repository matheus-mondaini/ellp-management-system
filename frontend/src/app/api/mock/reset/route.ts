import { NextResponse } from "next/server";

import { resetMockState } from "../_state";

export async function POST() {
  resetMockState();
  return NextResponse.json({ ok: true });
}
