import { NextResponse } from "next/server";

import { listMockTemas } from "../_state";

export function GET() {
  return NextResponse.json(listMockTemas());
}
