"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Download, Filter, Calendar, Award } from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type RelatorioCertificados } from "@/types/api";

export default function RelatoriosCertificadosPage() {
  const api = useApi();
  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");

  const { data: relatorio, isLoading } = useQuery({
    queryKey: ["relatorio-certificados", dataInicio, dataFim],
    queryFn: () => {
      const params = new URLSearchParams();
      if (dataInicio) params.append("data_inicio", dataInicio);
      if (dataFim) params.append("data_fim", dataFim);
      return api<RelatorioCertificados>(`/relatorios/certificados?${params.toString()}`);
    },
  });

  const handleExportCSV = () => {
    if (!relatorio) return;
    
    const headers = ["Aluno", "Oficina", "Data Emissão", "Percentual Presença", "Hash"];
    const rows = relatorio.certificados.map((c) => [
      c.aluno_nome,
      c.oficina_titulo,
      c.data_emissao,
      `${c.percentual_presenca}%`,
      c.hash_validacao,
    ]);
    
    const csv = [headers, ...rows].map((row) => row.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `certificados-${format(new Date(), "yyyy-MM-dd")}.csv`;
    a.click();
  };

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-014</p>
        <h1 className="text-3xl font-semibold text-white">Relatórios de Certificados</h1>
        <p className="text-sm text-slate-300">
          Visualize e exporte relatórios de certificados emitidos.
        </p>
      </div>

      <div className="rounded-2xl bg-white/5 p-6 space-y-4">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <Filter className="h-5 w-5" />
          Filtrar por Período
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Data Início"
            type="date"
            value={dataInicio}
            onChange={(e) => setDataInicio(e.target.value)}
          />
          <Input
            label="Data Fim"
            type="date"
            value={dataFim}
            onChange={(e) => setDataFim(e.target.value)}
          />
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
              <h2 className="text-xl font-semibold text-white">Certificados Emitidos</h2>
              <p className="text-sm text-slate-400">
                {dataInicio && dataFim
                  ? `${format(new Date(dataInicio), "dd/MM/yyyy", { locale: ptBR })} - ${format(
                      new Date(dataFim),
                      "dd/MM/yyyy",
                      { locale: ptBR }
                    )}`
                  : "Todos os períodos"}
              </p>
            </div>
            <Button onClick={handleExportCSV} className="gap-2">
              <Download className="h-4 w-4" />
              Exportar CSV
            </Button>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Total de Certificados</p>
              <p className="text-2xl font-bold text-white">{relatorio.total_certificados}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Oficinas com Certificados</p>
              <p className="text-2xl font-bold text-white">{relatorio.total_oficinas}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
              <p className="text-sm text-slate-400">Presença Média</p>
              <p className="text-2xl font-bold text-emerald-400">{relatorio.media_presenca}%</p>
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
                    Oficina
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Data Emissão
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Presença
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {relatorio.certificados.map((cert: any) => (
                  <tr key={cert.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-sm font-medium text-white">{cert.aluno_nome}</p>
                        <p className="text-xs text-slate-400">{cert.aluno_email}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-white">{cert.oficina_titulo}</p>
                      <p className="text-xs text-slate-400">{cert.oficina_periodo}</p>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm text-slate-300">
                        <Calendar className="h-4 w-4" />
                        {format(new Date(cert.data_emissao), "dd/MM/yyyy", { locale: ptBR })}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="text-sm font-semibold text-emerald-400">
                        {cert.percentual_presenca}%
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => window.open(`/api/mock/certificados/${cert.id}/download`, "_blank")}
                        >
                          <Download className="h-3 w-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => window.open(`/validar/${cert.hash_validacao}`, "_blank")}
                        >
                          <Award className="h-3 w-3" />
                        </Button>
                      </div>
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
