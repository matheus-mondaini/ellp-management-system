import { NextResponse } from "next/server";

import { getMockCertificadoValidation } from "../../../_state";

export function GET(
  _request: Request,
  { params }: { params: { hash: string } },
) {
  const certificado = getMockCertificadoValidation(params.hash);
  if (!certificado) {
    return NextResponse.json({ detail: "Certificado não encontrado" }, { status: 404 });
  }

  return NextResponse.json(certificado);
}
