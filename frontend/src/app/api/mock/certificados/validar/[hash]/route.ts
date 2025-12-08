import { NextResponse } from "next/server";

import { getMockCertificadoValidation } from "../../../_state";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ hash: string }> },
) {
  const { hash } = await params;
  const certificado = getMockCertificadoValidation(hash);
  if (!certificado) {
    return NextResponse.json({ detail: "Certificado não encontrado" }, { status: 404 });
  }

  return NextResponse.json(certificado);
}
