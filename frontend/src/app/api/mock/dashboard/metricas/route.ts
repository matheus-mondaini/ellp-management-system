import { NextResponse } from "next/server";

import { getDashboardMetrics } from "../../_state";

export function GET() {
  return NextResponse.json(getDashboardMetrics());
}
