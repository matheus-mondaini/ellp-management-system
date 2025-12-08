"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Activity, Award, CalendarRange, ClipboardCheck, Users2 } from "lucide-react";

import { BurndownChart } from "@/components/charts/burndown";
import { MetricCard } from "@/components/charts/metric-card";
import { PresenceTrend } from "@/components/charts/presence-trend";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type DashboardMetrics } from "@/types/api";

const metricConfig = [
  { key: "oficinas_ativas", label: "Oficinas ativas", icon: <CalendarRange className="h-4 w-4" /> },
  { key: "total_inscricoes", label: "Inscrições totais", icon: <Users2 className="h-4 w-4" /> },
  { key: "certificados_emitidos", label: "Certificados emitidos", icon: <Award className="h-4 w-4" /> },
  { key: "presenca_media_geral", label: "Presença média", icon: <ClipboardCheck className="h-4 w-4" /> },
] as const;

export default function DashboardPage() {
  const api = useApi();
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["dashboard-metricas"],
    queryFn: () => api<DashboardMetrics>("/dashboard/metricas"),
  });

  const progress = useMemo(() => {
    if (!data) {
      return null;
    }
    return {
      concluidos: data.inscritos_concluidos,
      total: data.total_inscricoes,
      percentual: data.total_inscricoes
        ? Math.round((data.inscritos_concluidos / data.total_inscricoes) * 100)
        : 0,
    };
  }, [data]);

  return (
    <div className="space-y-8">
      <div className="space-y-1">
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Visão geral</p>
        <h1 className="text-3xl font-semibold text-white">Dashboard operacional</h1>
        <p className="text-sm text-slate-300">
          Métricas em tempo real das oficinas lógicas e emissão de certificados (RF-022).
        </p>
      </div>

      {isError && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
          Falha ao carregar métricas: {(error as Error)?.message ?? "erro inesperado"}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metricConfig.map((config) => (
          <MetricCard
            key={config.key}
            label={config.label}
            icon={config.icon}
            value={isLoading ? <Skeleton className="h-10 w-24" /> : formatMetricValue(config.key, data)}
            trend={config.key === "presenca_media_geral" && data ? `${data.presenca_media_geral.toFixed(1)}%` : undefined}
          />
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2 bg-white/5 text-white">
          <BurndownChart />
        </Card>
        <Card className="bg-white/5 text-white">
          <PresenceTrend />
        </Card>
      </div>

      {progress && (
        <Card
          title="Conclusão das inscrições"
          description="Relação entre alunos concluintes e inscritos em todas as oficinas"
          className="bg-white/5 text-white"
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-300">Alunos concluintes</span>
              <span className="font-semibold text-white">
                {progress.concluidos}/{progress.total} ({progress.percentual}%)
              </span>
            </div>
            <div className="h-3 w-full rounded-full bg-white/10">
              <div
                className="h-3 rounded-full bg-gradient-to-r from-emerald-400 to-sky-400"
                style={{ width: `${progress.percentual}%` }}
              />
            </div>
            <div className="flex gap-4 text-xs uppercase tracking-[0.3em] text-slate-400">
              <span>Atualizado em {new Date(data?.ultima_atualizacao ?? Date.now()).toLocaleString("pt-BR")}</span>
              <span className="flex items-center gap-2 text-emerald-300">
                <Activity className="h-3 w-3" />
                Monitorado
              </span>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

function formatMetricValue(key: (typeof metricConfig)[number]["key"], data?: DashboardMetrics) {
  if (!data) {
    return "—";
  }
  switch (key) {
    case "oficinas_ativas":
      return data.oficinas_ativas;
    case "total_inscricoes":
      return data.total_inscricoes;
    case "certificados_emitidos":
      return data.certificados_emitidos;
    case "presenca_media_geral":
      return `${data.presenca_media_geral.toFixed(1)}%`;
    default:
      return "—";
  }
}
