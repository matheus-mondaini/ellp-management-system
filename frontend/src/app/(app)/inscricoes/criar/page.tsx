"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useApi } from "@/hooks/use-api";
import { type Oficina, type UserSummary } from "@/types/api";

const inscricaoSchema = z.object({
  aluno_id: z.string().uuid("Selecione um aluno"),
  oficina_id: z.string().uuid("Selecione uma oficina"),
});

type InscricaoFormData = z.infer<typeof inscricaoSchema>;

export default function CriarInscricaoPage() {
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<InscricaoFormData>({
    resolver: zodResolver(inscricaoSchema),
  });

  const { data: alunos } = useQuery({
    queryKey: ["alunos"],
    queryFn: () => api<UserSummary[]>("/users/alunos"),
  });

  const { data: oficinas } = useQuery({
    queryKey: ["oficinas"],
    queryFn: () => api<Oficina[]>("/oficinas?status=inscricoes_abertas"),
  });

  const mutation = useMutation({
    mutationFn: (data: InscricaoFormData) => api("/inscricoes", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inscricoes"] });
      router.push("/oficinas");
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const onSubmit = (data: InscricaoFormData) => {
    setError(null);
    mutation.mutate(data);
  };

  return (
    <div className="space-y-8">
      <div>
        <Button variant="ghost" onClick={() => router.back()} className="mb-4 text-slate-300 hover:text-white">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-005</p>
        <h1 className="text-3xl font-semibold text-white">Inscrever Aluno</h1>
        <p className="text-sm text-slate-300">
          Inscrição administrativa respeitando capacidade máxima da oficina.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
          {error}
        </div>
      )}

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="rounded-2xl bg-white/5 p-6 space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label htmlFor="aluno" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">
                Aluno
              </label>
              <select
                id="aluno"
                {...form.register("aluno_id")}
                className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900"
              >
                <option value="">Selecione um aluno...</option>
                {alunos?.map((aluno) => (
                  <option key={aluno.id} value={aluno.id}>
                    {aluno.nome_completo}
                  </option>
                ))}
              </select>
              {form.formState.errors.aluno_id && (
                <span className="block text-xs text-rose-500 mt-1">
                  {form.formState.errors.aluno_id.message}
                </span>
              )}
            </div>

            <div>
              <label htmlFor="oficina" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">
                Oficina
              </label>
              <select
                id="oficina"
                {...form.register("oficina_id")}
                className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900"
              >
                <option value="">Selecione uma oficina...</option>
                {oficinas?.map((oficina) => (
                  <option key={oficina.id} value={oficina.id}>
                    {oficina.titulo} - {oficina.vagas_disponiveis} vagas disponíveis
                  </option>
                ))}
              </select>
              {form.formState.errors.oficina_id && (
                <span className="block text-xs text-rose-500 mt-1">
                  {form.formState.errors.oficina_id.message}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-4">
          <Button type="button" variant="ghost" onClick={() => router.back()} disabled={mutation.isPending}>
            Cancelar
          </Button>
          <Button type="submit" loading={mutation.isPending}>
            Inscrever Aluno
          </Button>
        </div>
      </form>
    </div>
  );
}
