import type { ReactNode } from "react";
import { notFound } from "next/navigation";

import { apiFetch } from "@/lib/api-client";
import { env } from "@/lib/env";
import { format } from "date-fns";
import ptBR from "date-fns/locale/pt-BR";
import { CertificadoValidacao } from "@/types/api";
import { cn } from "@/lib/utils";
import { CopyClipboardButton } from "@/components/certificados/copy-clipboard-button";

async function getCertificado(hash: string) {
  try {
    return await apiFetch<CertificadoValidacao>(`/certificados/validar/${hash}`);
  } catch (error) {
    if ((error as { status?: number }).status === 404) {
      notFound();
    }
    throw error;
  }
}

function Field({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="space-y-1 rounded-2xl bg-white/5 p-4 text-left">
      <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{label}</p>
      <p className="text-base font-semibold text-white">{value}</p>
    </div>
  );
}

export default async function CertificateValidationPage({ params }: { params: Promise<{ hash: string }> }) {
  const { hash } = await params;
  const certificado = await getCertificado(hash);
  const downloadUrl = certificado.arquivo_pdf_url;

  return (
    <section className="space-y-8 text-white">
      <header className="space-y-1">
        <p className="text-sm uppercase tracking-[0.3em] text-emerald-300">RF-009</p>
        <h2 className="text-3xl font-semibold">Resultado da validação</h2>
        <p className="text-slate-300">Hash verificado em {env.apiUrl}</p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        <Field label="Participante" value={`${certificado.participante_nome} (${certificado.participante_tipo})`} />
        <Field label="Oficina" value={certificado.oficina_titulo} />
        <Field label="Carga horária" value={`${certificado.carga_horaria_certificada ?? "–"}h`} />
        <Field label="Presença" value={certificado.percentual_presenca_certificado ? `${certificado.percentual_presenca_certificado.toFixed(1)}%` : "–"} />
        <Field
          label="Emitido em"
          value={format(new Date(certificado.data_emissao), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
        />
        <Field label="Código de verificação" value={certificado.codigo_verificacao} />
      </div>

      <div
        className={cn(
          "rounded-3xl border-2 p-5 text-sm font-semibold",
          certificado.revogado ? "border-rose-400 text-rose-200" : "border-emerald-400 text-emerald-200",
        )}
      >
        {certificado.revogado ? (
          <p>Certificado revogado — {certificado.motivo_revogacao ?? "motivo não informado"}</p>
        ) : (
          <p>Certificado válido — hash {certificado.hash_validacao}</p>
        )}
      </div>

      <div className="flex flex-wrap gap-4 text-sm">
        <CopyClipboardButton value={certificado.codigo_verificacao}>
          Copiar código de verificação
        </CopyClipboardButton>
        {downloadUrl ? (
          <a
            href={downloadUrl}
            target="_blank"
            rel="noreferrer"
            className="rounded-full border border-emerald-300/60 px-4 py-2 text-emerald-200 transition hover:border-emerald-200 hover:text-emerald-100"
          >
            Baixar PDF
          </a>
        ) : null}
      </div>
    </section>
  );
}
