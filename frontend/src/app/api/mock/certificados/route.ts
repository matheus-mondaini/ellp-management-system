import { NextResponse } from "next/server";

import { listMockCertificados } from "../_state";

export function GET() {
  return NextResponse.json(listMockCertificados());
}
