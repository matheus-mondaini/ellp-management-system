import { NextResponse } from "next/server";

import { getMockCertificadoById } from "../../../_state";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ certificadoId: string }> },
) {
  const { certificadoId } = await params;
  const certificado = getMockCertificadoById(certificadoId);
  if (!certificado) {
    return NextResponse.json({ detail: "Certificado não encontrado" }, { status: 404 });
  }

  return NextResponse.json({
    arquivo_pdf_url: certificado.arquivo_pdf_url,
    arquivo_pdf_nome: certificado.arquivo_pdf_nome,
    hash_validacao: certificado.hash_validacao,
    codigo_verificacao: certificado.codigo_verificacao,
  });
}
