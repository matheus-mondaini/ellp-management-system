"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Calendar, Filter, Plus, X } from "lucide-react";

import { OficinaForm } from "@/components/forms/oficina-form";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type Oficina, type OficinaStatus } from "@/types/api";

const statusLabels: Record<OficinaStatus, string> = {
  planejada: "Planejada",
  inscricoes_abertas: "Inscrições",
  em_andamento: "Em andamento",
  concluida: "Concluída",
  cancelada: "Cancelada",
};

const statusColors: Record<OficinaStatus, string> = {
  planejada: "bg-slate-600/30 text-slate-200",
  inscricoes_abertas: "bg-emerald-500/20 text-emerald-200",
  em_andamento: "bg-sky-500/20 text-sky-100",
  concluida: "bg-emerald-700/30 text-emerald-100",
  cancelada: "bg-rose-500/20 text-rose-100",
};

export default function OficinasPage() {
  const api = useApi();
  const [statusFilter, setStatusFilter] = useState<OficinaStatus | "todas">("todas");
  const [formOpen, setFormOpen] = useState(false);

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["oficinas"],
    queryFn: () => api<Oficina[]>("/oficinas"),
  });

  const filtered = useMemo(() => {
    if (!data) return [];
    if (statusFilter === "todas") return data;
    return data.filter((oficina) => oficina.status === statusFilter);
  }, [data, statusFilter]);

  return (
    <div className="space-y-8">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Operação</p>
          <h1 className="text-3xl font-semibold text-white">Oficinas extensionistas</h1>
          <p className="text-sm text-slate-300">Controle unificado de turmas, status e vagas.</p>
        </div>
        <Button
          type="button"
          onClick={() => setFormOpen(true)}
          className="rounded-full bg-emerald-500/80 px-6 py-3 text-white shadow-lg shadow-emerald-500/30"
        >
          <Plus className="h-4 w-4" />
          Nova oficina
        </Button>
      </header>

      <section className="rounded-3xl border border-white/10 bg-white/5 p-6 text-sm text-white">
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-slate-400">
            <Filter className="h-3.5 w-3.5" /> Filtros de status
          </span>
          {(["todas", ...Object.keys(statusLabels)] as Array<OficinaStatus | "todas">).map((status) => (
            <button
              key={status}
              type="button"
              onClick={() => setStatusFilter(status)}
              className={`rounded-full border px-4 py-1 text-xs font-semibold uppercase tracking-[0.3em] transition ${
                statusFilter === status
                  ? "border-white bg-white/20 text-white"
                  : "border-white/20 text-white/60 hover:text-white"
              }`}
            >
              {status === "todas" ? "Todas" : statusLabels[status]}
            </button>
          ))}
        </div>

        {isError && (
          <div className="mt-4 rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-100">
            Falha ao carregar oficinas: {(error as Error)?.message ?? "erro inesperado"}
          </div>
        )}

        <div className="mt-6 overflow-hidden rounded-2xl border border-white/10">
          <table className="w-full table-auto text-left text-sm">
            <thead className="bg-white/5 text-xs uppercase tracking-[0.3em] text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Oficina</th>
                <th className="px-4 py-3 font-medium">Período</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Vagas</th>
              </tr>
            </thead>
            <tbody>
              {isLoading && (
                <tr>
                  <td colSpan={4} className="px-4 py-8">
                    <Skeleton className="h-10 w-full bg-white/10" />
                  </td>
                </tr>
              )}
              {!isLoading && filtered.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-slate-400">
                    Nenhuma oficina encontrada para o filtro selecionado.
                  </td>
                </tr>
              )}
              {filtered.map((oficina) => (
                <tr key={oficina.id} className="border-t border-white/5">
                  <td className="px-4 py-4">
                    <div className="font-semibold text-white">{oficina.titulo}</div>
                    <p className="text-xs text-slate-400">{oficina.local}</p>
                  </td>
                  <td className="px-4 py-4 text-slate-200">
                    <div className="flex items-center gap-2 text-xs">
                      <Calendar className="h-4 w-4 text-white/50" />
                      {formatDateRange(oficina.data_inicio, oficina.data_fim)}
                    </div>
                  </td>
                  <td className="px-4 py-4">
                    <Badge className={statusColors[oficina.status]}>{statusLabels[oficina.status]}</Badge>
                  </td>
                  <td className="px-4 py-4 text-sm text-slate-200">
                    {oficina.vagas_disponiveis} vagas livres
                  </td>
                  <td className="px-4 py-4">
                    <div className="flex gap-2">
                      <Button
                        onClick={() => window.location.href = `/oficinas/${oficina.id}`}
                        className="text-xs"
                      >
                        Ver
                      </Button>
                      <Button
                        onClick={() => window.location.href = `/oficinas/${oficina.id}/editar`}
                        className="text-xs"
                      >
                        Editar
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {formOpen && (
        <div className="fixed inset-0 z-20 flex items-center justify-center bg-slate-950/80 p-4">
          <div className="relative max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-3xl border border-white/10 bg-slate-900/90 p-8 text-white shadow-2xl">
            <button
              type="button"
              onClick={() => setFormOpen(false)}
              className="absolute right-6 top-6 text-white/60 transition hover:text-white"
            >
              <X className="h-5 w-5" />
            </button>
            <h2 className="text-2xl font-semibold">Nova oficina</h2>
            <p className="text-sm text-slate-300">Cadastre oficinas alinhadas ao plano extensionista.</p>
            <OficinaForm
              className="mt-6"
              onCreated={() => {
                setFormOpen(false);
                void refetch();
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function formatDateRange(inicio: string, fim: string) {
  const formatter = new Intl.DateTimeFormat("pt-BR", { day: "2-digit", month: "short" });
  return `${formatter.format(new Date(inicio))} – ${formatter.format(new Date(fim))}`;
}
