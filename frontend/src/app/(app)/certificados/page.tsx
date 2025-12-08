"use client";

import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { CheckCircle2, Download, Filter, ShieldCheck, XCircle } from "lucide-react";

import { CopyClipboardButton } from "@/components/certificados/copy-clipboard-button";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type Certificado } from "@/types/api";

const tipoLabels: Record<Certificado["tipo"], string> = {
  conclusao_aluno: "Conclusão (Aluno)",
  participacao_tutor: "Participação (Tutor)",
};

export default function CertificadosPage() {
  const api = useApi();
  const [statusFilter, setStatusFilter] = useState<"todos" | "validos" | "revogados">("todos");
  const [validationBaseUrl, setValidationBaseUrl] = useState("http://localhost:3000");

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["certificados"],
    queryFn: () => api<Certificado[]>("/certificados"),
  });

  const downloadMutation = useMutation({
    mutationFn: (certificadoId: string) => api<{ arquivo_pdf_url: string | null }>(`/certificados/${certificadoId}/download`),
    onSuccess: (result) => {
      if (result.arquivo_pdf_url) {
        window.open(result.arquivo_pdf_url, "_blank", "noopener,noreferrer");
      } else {
        window.alert("Arquivo ainda não disponível no storage");
      }
    },
    onError: (err) => {
      window.alert((err as Error)?.message ?? "Falha ao baixar certificado");
    },
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
      setValidationBaseUrl(window.location.origin);
    }
  }, []);

  const filtered = useMemo(() => {
    if (!data) return [];
    if (statusFilter === "todos") return data;
    return data.filter((certificado) => (statusFilter === "validos" ? !certificado.revogado : certificado.revogado));
  }, [data, statusFilter]);

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-008</p>
        <h1 className="text-3xl font-semibold text-white">Certificados e verificações</h1>
        <p className="text-sm text-slate-300">
          Gere PDFs, acompanhe hashes e mantenha o histórico de emissões alinhado ao backend FastAPI.
        </p>
      </div>

      <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-white">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-slate-400">
            <Filter className="h-3.5 w-3.5" /> Status dos certificados
          </div>
          <div className="flex gap-2">
            {["todos", "validos", "revogados"].map((status) => (
              <button
                key={status}
                type="button"
                onClick={() => setStatusFilter(status as typeof statusFilter)}
                className={`rounded-full border px-4 py-1 text-xs font-semibold uppercase tracking-[0.3em] transition ${
                  statusFilter === status
                    ? "border-white bg-white/20 text-white"
                    : "border-white/20 text-white/60 hover:text-white"
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </header>

        {isError && (
          <div className="mt-4 rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-100">
            Falha ao carregar certificados: {(error as Error)?.message ?? "erro inesperado"}
          </div>
        )}

        <div className="mt-6 overflow-hidden rounded-2xl border border-white/10">
          <table className="w-full table-auto text-sm">
            <thead className="bg-white/5 text-left text-xs uppercase tracking-[0.3em] text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Tipo</th>
                <th className="px-4 py-3 font-medium">Código</th>
                <th className="px-4 py-3 font-medium">Hash</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {isLoading && (
                <tr>
                  <td colSpan={5} className="px-4 py-8">
                    <Skeleton className="h-10 w-full bg-white/10" />
                  </td>
                </tr>
              )}
              {!isLoading && filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-slate-400">
                    Nenhum certificado no filtro selecionado.
                  </td>
                </tr>
              )}
              {filtered.map((certificado) => (
                <tr key={certificado.id} className="border-t border-white/5">
                  <td className="px-4 py-4">
                    <Badge className="bg-white/10 text-white">{tipoLabels[certificado.tipo]}</Badge>
                    <p className="text-xs text-slate-400">Emitido em {new Date(certificado.data_emissao).toLocaleDateString("pt-BR")}</p>
                  </td>
                  <td className="px-4 py-4">
                    <div className="flex items-center gap-2 text-sm text-white">
                      <ShieldCheck className="h-4 w-4 text-emerald-300" />
                      {certificado.codigo_verificacao}
                    </div>
                  </td>
                  <td className="px-4 py-4">
                    <CopyClipboardButton value={`${validationBaseUrl}/validar/${certificado.hash_validacao}`}>
                      Copiar link
                    </CopyClipboardButton>
                  </td>
                  <td className="px-4 py-4">
                    {certificado.revogado ? (
                      <span className="inline-flex items-center gap-2 text-sm text-rose-200">
                        <XCircle className="h-4 w-4" /> Revogado
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-2 text-sm text-emerald-200">
                        <CheckCircle2 className="h-4 w-4" /> Válido
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-4">
                    <div className="flex flex-wrap gap-2">
                      <CopyClipboardButton value={certificado.codigo_verificacao}>
                        Copiar código
                      </CopyClipboardButton>
                      <Button
                        type="button"
                        variant="ghost"
                        className="rounded-full border border-white/20 px-4 text-xs uppercase tracking-[0.3em] text-white/70 hover:text-white"
                        onClick={() => downloadMutation.mutate(certificado.id)}
                        disabled={downloadMutation.isPending}
                      >
                        <Download className="h-4 w-4" />
                        Baixar PDF
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
