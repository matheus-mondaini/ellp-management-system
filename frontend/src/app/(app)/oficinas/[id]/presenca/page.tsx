"use client";

import { use, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Check, X } from "lucide-react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { useApi } from "@/hooks/use-api";
import { type Inscricao } from "@/types/api";

export default function PresencaPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: oficinaId } = use(params);
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const [dataAula, setDataAula] = useState<string>(new Date().toISOString().split("T")[0]);
  const [presencas, setPresencas] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<string | null>(null);

  const { data: inscricoes, isLoading } = useQuery({
    queryKey: ["oficina-inscricoes", oficinaId],
    queryFn: () => api<Inscricao[]>(`/oficinas/${oficinaId}/alunos`),
  });

  const mutation = useMutation({
    mutationFn: (data: { inscricao_id: string; data_aula: string; presente: boolean }[]) =>
      api("/presencas/lote", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["oficina-inscricoes", oficinaId] });
      setError(null);
      alert("Presenças registradas com sucesso!");
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const togglePresenca = (inscricaoId: string) => {
    setPresencas((prev) => ({
      ...prev,
      [inscricaoId]: !prev[inscricaoId],
    }));
  };

  const marcarTodos = (presente: boolean) => {
    const novasPresencas: Record<string, boolean> = {};
    inscricoes?.forEach((insc) => {
      novasPresencas[insc.id] = presente;
    });
    setPresencas(novasPresencas);
  };

  const handleSubmit = () => {
    if (!dataAula) {
      setError("Selecione a data da aula");
      return;
    }

    const payload = Object.entries(presencas).map(([inscricaoId, presente]) => ({
      inscricao_id: inscricaoId,
      data_aula: dataAula,
      presente,
    }));

    mutation.mutate(payload);
  };

  return (
    <div className="space-y-8">
      <div>
        <Button variant="ghost" onClick={() => router.back()} className="mb-4 text-slate-300 hover:text-white">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-007</p>
        <h1 className="text-3xl font-semibold text-white">Registrar Presença</h1>
        <p className="text-sm text-slate-300">
          Marque os alunos presentes na aula. O percentual será calculado automaticamente.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
          {error}
        </div>
      )}

      <div className="rounded-2xl bg-white/5 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <label htmlFor="data-aula" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">
              Data da aula
            </label>
            <input
              id="data-aula"
              type="date"
              value={dataAula}
              onChange={(e) => setDataAula(e.target.value)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900"
            />
          </div>
          <div className="flex gap-2">
            <Button onClick={() => marcarTodos(true)} variant="ghost">
              <Check className="mr-2 h-4 w-4" />
              Marcar todos
            </Button>
            <Button onClick={() => marcarTodos(false)} variant="ghost">
              <X className="mr-2 h-4 w-4" />
              Desmarcar todos
            </Button>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center text-slate-400">Carregando alunos inscritos...</div>
      ) : (
        <div className="space-y-2">
          {inscricoes?.map((inscricao) => (
            <button
              key={inscricao.id}
              type="button"
              onClick={() => togglePresenca(inscricao.id)}
              className={`w-full rounded-2xl border p-4 text-left transition ${
                presencas[inscricao.id]
                  ? "border-emerald-500/40 bg-emerald-500/10"
                  : "border-white/10 bg-white/5"
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">{inscricao.aluno_nome}</p>
                  <p className="text-sm text-slate-400">Presença atual: {inscricao.percentual_presenca}%</p>
                </div>
                <div className={`rounded-full p-2 ${presencas[inscricao.id] ? "bg-emerald-500" : "bg-slate-600"}`}>
                  {presencas[inscricao.id] ? (
                    <Check className="h-5 w-5 text-white" />
                  ) : (
                    <X className="h-5 w-5 text-white" />
                  )}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}

      <div className="flex justify-end">
        <Button onClick={handleSubmit} loading={mutation.isPending} disabled={!dataAula}>
          Salvar Presenças
        </Button>
      </div>
    </div>
  );
}
