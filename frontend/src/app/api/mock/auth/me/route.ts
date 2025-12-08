import { NextResponse } from "next/server";

import { getUserFromToken } from "../../_state";

export function GET(request: Request) {
  const authHeader = request.headers.get("authorization") ?? "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) {
    return NextResponse.json({ detail: "Token ausente" }, { status: 401 });
  }

  const user = getUserFromToken(token);
  if (!user) {
    return NextResponse.json({ detail: "Sessão inválida" }, { status: 401 });
  }

  return NextResponse.json(user);
}
