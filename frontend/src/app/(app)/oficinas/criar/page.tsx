"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useApi } from "@/hooks/use-api";
import { type UserSummary } from "@/types/api";

const oficinaSchema = z.object({
  titulo: z.string().min(5, "Título deve ter no mínimo 5 caracteres"),
  descricao: z.string().min(10, "Descrição deve ter no mínimo 10 caracteres"),
  carga_horaria: z.coerce.number().min(1, "Carga horária mínima de 1 hora"),
  capacidade_maxima: z.coerce.number().min(1, "Capacidade mínima de 1 aluno"),
  data_inicio: z.string(),
  data_fim: z.string(),
  local: z.string().min(3, "Local deve ser especificado"),
  professor_id: z.string().uuid("Selecione um professor"),
});

type OficinaFormData = z.infer<typeof oficinaSchema>;

export default function CriarOficinaPage() {
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<OficinaFormData>({
    resolver: zodResolver(oficinaSchema),
  });

  const { data: professores } = useQuery({
    queryKey: ["professores"],
    queryFn: () => api<UserSummary[]>("/users?role=professor"),
  });

  const mutation = useMutation({
    mutationFn: (data: OficinaFormData) => api("/oficinas", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["oficinas"] });
      router.push("/oficinas");
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const onSubmit = (data: OficinaFormData) => {
    setError(null);
    mutation.mutate(data);
  };

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
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-003</p>
        <h1 className="text-3xl font-semibold text-white">Criar Oficina</h1>
        <p className="text-sm text-slate-300">
          Cadastro de oficina com período, capacidade e professor responsável.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
          {error}
        </div>
      )}

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="rounded-2xl bg-white/5 p-6 space-y-4">
          <h3 className="font-semibold text-white">Informações Básicas</h3>
          <div className="grid gap-4">
            <Input
              label="Título da oficina"
              placeholder="Ex: Scratch Básico - Turma Manhã"
              {...form.register("titulo")}
              error={form.formState.errors.titulo?.message}
            />
            <div className="grid md:grid-cols-3 gap-4">
              <Input
                label="Carga horária (horas)"
                type="number"
                {...form.register("carga_horaria")}
                error={form.formState.errors.carga_horaria?.message}
              />
              <Input
                label="Capacidade máxima"
                type="number"
                {...form.register("capacidade_maxima")}
                error={form.formState.errors.capacidade_maxima?.message}
              />
              <div>
                <label htmlFor="nova-oficina-professor" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">
                  Professor responsável
                </label>
                <select
                  id="nova-oficina-professor"
                  {...form.register("professor_id")}
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900"
                >
                  <option value="">Selecione...</option>
                  {professores?.map((prof) => (
                    <option key={prof.id} value={prof.id}>
                      {prof.nome_completo}
                    </option>
                  ))}
                </select>
                {form.formState.errors.professor_id && (
                  <span className="block text-xs text-rose-500 mt-1">
                    {form.formState.errors.professor_id.message}
                  </span>
                )}
              </div>
            </div>
            <textarea
              {...form.register("descricao")}
              placeholder="Descreva os objetivos, conteúdo e metodologia da oficina..."
              rows={4}
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 placeholder:text-slate-400"
            />
            {form.formState.errors.descricao && (
              <span className="text-xs text-rose-500">{form.formState.errors.descricao.message}</span>
            )}
          </div>
        </div>

        <div className="rounded-2xl bg-white/5 p-6 space-y-4">
          <h3 className="font-semibold text-white">Período e Local</h3>
          <div className="grid md:grid-cols-3 gap-4">
            <Input
              label="Data de início"
              type="date"
              {...form.register("data_inicio")}
              error={form.formState.errors.data_inicio?.message}
            />
            <Input
              label="Data de término"
              type="date"
              {...form.register("data_fim")}
              error={form.formState.errors.data_fim?.message}
            />
            <Input
              label="Local"
              placeholder="Ex: UTFPR - Lab 01"
              {...form.register("local")}
              error={form.formState.errors.local?.message}
            />
          </div>
        </div>

        <div className="flex justify-end gap-4">
          <Button
            type="button"
            variant="ghost"
            onClick={() => router.back()}
            disabled={mutation.isPending}
          >
            Cancelar
          </Button>
          <Button type="submit" loading={mutation.isPending}>
            Criar Oficina
          </Button>
        </div>
      </form>
    </div>
  );
}
