"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Download, Users } from "lucide-react";
import { format } from "date-fns";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type Oficina, type RelatorioFrequencia } from "@/types/api";

export default function RelatoriosFrequenciaPage() {
  const api = useApi();
  const [selectedOficinaId, setSelectedOficinaId] = useState<string | null>(null);

  const { data: oficinas } = useQuery({
    queryKey: ["oficinas"],
    queryFn: () => api<Oficina[]>("/oficinas"),
  });

  const { data: relatorio, isLoading } = useQuery({
    queryKey: ["relatorio-frequencia", selectedOficinaId],
    queryFn: () => api<RelatorioFrequencia>(`/relatorios/frequencia/${selectedOficinaId}`),
    enabled: !!selectedOficinaId,
  });

  const handleExportCSV = () => {
    if (!relatorio) return;
    
    const headers = ["Nome", "Email", "Status", "Presenças", "Total Sessões", "Percentual"];
    const rows = relatorio.inscricoes.map((i) => [
      i.aluno_nome,
      i.aluno_email,
      i.status,
      i.presencas,
      relatorio.total_sessoes,
      `${i.percentual}%`,
    ]);
    
    const csv = [headers, ...rows].map((row) => row.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `frequencia-${relatorio.oficina_titulo}-${format(new Date(), "yyyy-MM-dd")}.csv`;
    a.click();
  };

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-014</p>
        <h1 className="text-3xl font-semibold text-white">Relatórios de Frequência</h1>
        <p className="text-sm text-slate-300">
          Visualize e exporte relatórios de frequência por oficina.
        </p>
      </div>

      <div className="rounded-2xl bg-white/5 p-6 space-y-4">
        <h2 className="text-lg font-semibold text-white">Selecione uma Oficina</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {oficinas?.map((oficina) => (
            <button
              key={oficina.id}
              type="button"
              onClick={() => setSelectedOficinaId(oficina.id)}
              className={`rounded-xl border p-4 text-left transition ${
                selectedOficinaId === oficina.id
                  ? "border-emerald-400 bg-emerald-400/10"
                  : "border-white/10 bg-white/5 hover:bg-white/10"
              }`}
            >
              <h3 className="font-semibold text-white">{oficina.titulo}</h3>
              <p className="text-sm text-slate-400">
                {format(new Date(oficina.data_inicio), "dd/MM/yyyy")} - {format(new Date(oficina.data_fim), "dd/MM/yyyy")}
              </p>
              <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                <Users className="h-3 w-3" />
                <span>{oficina.vagas_disponiveis}/{oficina.total_inscritos} inscritos</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {isLoading && (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      )}

      {relatorio && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white">{relatorio.oficina_titulo}</h2>
              <p className="text-sm text-slate-400">{relatorio.oficina_periodo}</p>
            </div>
            <Button onClick={handleExportCSV} className="gap-2">
              <Download className="h-4 w-4" />
              Exportar CSV
            </Button>
          </div>

          <div className="grid gap-4 md:grid-cols-4">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Total de Inscritos</p>
              <p className="text-2xl font-bold text-white">{relatorio.total_inscritos}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Total de Sessões</p>
              <p className="text-2xl font-bold text-white">{relatorio.total_sessoes}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Presença Média</p>
              <p className="text-2xl font-bold text-emerald-400">{relatorio.media_presenca}%</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Certificados Emitidos</p>
              <p className="text-2xl font-bold text-white">{relatorio.certificados_emitidos}</p>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
            <table className="w-full">
              <thead className="bg-white/5">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Aluno
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Presenças
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Percentual
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {relatorio.inscricoes.map((inscricao) => (
                  <tr key={inscricao.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-sm font-medium text-white">{inscricao.aluno_nome}</p>
                        <p className="text-xs text-slate-400">{inscricao.aluno_email}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <Badge>{inscricao.status}</Badge>
                    </td>
                    <td className="px-6 py-4 text-right text-sm text-white">
                      {inscricao.presencas}/{relatorio.total_sessoes}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span
                        className={`text-sm font-semibold ${
                          inscricao.percentual >= 75
                            ? "text-emerald-400"
                            : inscricao.percentual >= 50
                            ? "text-yellow-400"
                            : "text-red-400"
                        }`}
                      >
                        {inscricao.percentual}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
