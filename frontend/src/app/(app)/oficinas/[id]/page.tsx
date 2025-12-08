"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Calendar, MapPin, Users, Clock, UserCheck } from "lucide-react";
import { useRouter } from "next/navigation";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type Oficina, type Inscricao } from "@/types/api";

const statusLabels: Record<Oficina["status"], string> = {
  planejada: "Planejada",
  inscricoes_abertas: "Inscrições Abertas",
  em_andamento: "Em Andamento",
  concluida: "Concluída",
  cancelada: "Cancelada",
};

export default function OficinaDetalhesPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const api = useApi();

  const { data: oficina, isLoading: loadingOficina } = useQuery({
    queryKey: ["oficina", id],
    queryFn: () => api<Oficina>(`/oficinas/${id}`),
  });

  const { data: inscricoes, isLoading: loadingInscricoes } = useQuery({
    queryKey: ["oficina-inscricoes", id],
    queryFn: () => api<Inscricao[]>(`/oficinas/${id}/alunos`),
    enabled: !!oficina,
  });

  if (loadingOficina) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!oficina) {
    return (
      <div className="text-center">
        <p className="text-slate-400">Oficina não encontrada</p>
      </div>
    );
  }

  const vagasOcupadas = inscricoes?.length || 0;
  const vagasDisponiveis = oficina.capacidade_maxima - vagasOcupadas;

  return (
    <div className="space-y-8">
      <div>
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="mb-4 text-slate-300 hover:text-white"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Oficina</p>
            <h1 className="text-3xl font-semibold text-white">{oficina.titulo}</h1>
            <p className="text-sm text-slate-300 mt-1">{oficina.descricao}</p>
          </div>
          <Badge className="text-sm">
            {statusLabels[oficina.status]}
          </Badge>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-2xl bg-white/5 p-4">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <Calendar className="h-4 w-4" />
            <span className="text-xs uppercase tracking-wide">Período</span>
          </div>
          <p className="text-white font-semibold">
            {format(new Date(oficina.data_inicio), "dd/MM/yyyy", { locale: ptBR })} até{" "}
            {format(new Date(oficina.data_fim), "dd/MM/yyyy", { locale: ptBR })}
          </p>
        </div>

        <div className="rounded-2xl bg-white/5 p-4">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <MapPin className="h-4 w-4" />
            <span className="text-xs uppercase tracking-wide">Local</span>
          </div>
          <p className="text-white font-semibold">{oficina.local}</p>
        </div>

        <div className="rounded-2xl bg-white/5 p-4">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <Users className="h-4 w-4" />
            <span className="text-xs uppercase tracking-wide">Vagas</span>
          </div>
          <p className="text-white font-semibold">
            {vagasOcupadas} / {oficina.capacidade_maxima}
          </p>
          <p className="text-xs text-slate-400 mt-1">
            {vagasDisponiveis > 0 ? `${vagasDisponiveis} disponíveis` : "Esgotado"}
          </p>
        </div>

        <div className="rounded-2xl bg-white/5 p-4">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <Clock className="h-4 w-4" />
            <span className="text-xs uppercase tracking-wide">Carga Horária</span>
          </div>
          <p className="text-white font-semibold">{oficina.carga_horaria}h</p>
        </div>
      </div>

      <div className="rounded-2xl bg-white/5 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">Alunos Inscritos</h2>
          <div className="flex gap-2">
            <Button onClick={() => router.push("/inscricoes/criar")}>
              Inscrever Aluno
            </Button>
            <Button onClick={() => router.push(`/oficinas/${id}/presenca`)}>
              <UserCheck className="mr-2 h-4 w-4" />
              Registrar Presença
            </Button>
          </div>
        </div>

        {loadingInscricoes ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-16 w-full" />
            ))}
          </div>
        ) : inscricoes && inscricoes.length > 0 ? (
          <div className="space-y-2">
            {inscricoes.map((inscricao) => (
              <div
                key={inscricao.id}
                className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 p-4"
              >
                <div>
                  <p className="font-semibold text-white">{inscricao.aluno_nome}</p>
                  <p className="text-sm text-slate-400">
                    Presença: {inscricao.percentual_presenca.toFixed(1)}% · Status:{" "}
                    {inscricao.status}
                  </p>
                </div>
                <Badge
                  className={
                    inscricao.percentual_presenca >= 75
                      ? "bg-emerald-500/20 text-emerald-100"
                      : "bg-rose-500/20 text-rose-100"
                  }
                >
                  {inscricao.percentual_presenca >= 75 ? "Apto" : "Insuficiente"}
                </Badge>
              </div>
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-white/10 bg-white/5 p-8 text-center">
            <p className="text-slate-400">Nenhum aluno inscrito ainda.</p>
          </div>
        )}
      </div>

      <div className="flex justify-end gap-2">
        <Button variant="ghost" onClick={() => router.push(`/oficinas/${id}/editar`)}>
          Editar Oficina
        </Button>
      </div>
    </div>
  );
}
