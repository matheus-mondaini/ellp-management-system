import { NextResponse } from "next/server";

import { listMockUsers } from "../_state";

export function GET() {
  return NextResponse.json(listMockUsers());
}
