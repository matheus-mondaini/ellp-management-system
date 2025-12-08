import { NextResponse } from "next/server";

import { authenticateMockUser } from "../../_state";

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as { email?: string; password?: string } | null;
  if (!body?.email || !body?.password) {
    return NextResponse.json({ detail: "Credenciais inválidas" }, { status: 400 });
  }

  const auth = authenticateMockUser(body.email, body.password);
  if (!auth) {
    return NextResponse.json({ detail: "E-mail ou senha incorretos" }, { status: 401 });
  }

  return NextResponse.json(auth.tokens);
}
