"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useApi } from "@/hooks/use-api";

const tutorSchema = z.object({
  nome_completo: z.string().min(3, "Nome deve ter no mínimo 3 caracteres"),
  email: z.string().email("E-mail inválido"),
  senha: z.string().min(8, "Senha deve ter no mínimo 8 caracteres"),
  telefone: z.string().optional(),
  instituicao_origem: z.string().optional(),
  curso: z.string().optional(),
});

type TutorFormData = z.infer<typeof tutorSchema>;

export default function CriarTutorPage() {
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<TutorFormData>({
    resolver: zodResolver(tutorSchema),
  });

  const mutation = useMutation({
    mutationFn: (data: TutorFormData) => api("/users/tutores", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
      router.push("/usuarios");
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const onSubmit = (data: TutorFormData) => {
    setError(null);
    mutation.mutate(data);
  };

  return (
    <div className="space-y-8">
      <div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => router.back()}
          className="mb-4 text-slate-300 hover:text-white"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-001 | RF-011</p>
        <h1 className="text-3xl font-semibold text-white">Cadastrar Tutor</h1>
        <p className="text-sm text-slate-300">
          Voluntário que auxilia nas oficinas (universitário, professor externo, etc).
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
            <Input
              label="Nome completo"
              {...form.register("nome_completo")}
              error={form.formState.errors.nome_completo?.message}
            />
            <Input
              label="E-mail"
              type="email"
              {...form.register("email")}
              error={form.formState.errors.email?.message}
            />
            <Input
              label="Senha"
              type="password"
              {...form.register("senha")}
              error={form.formState.errors.senha?.message}
            />
            <Input
              label="Telefone"
              {...form.register("telefone")}
              error={form.formState.errors.telefone?.message}
            />
            <Input
              label="Instituição de origem"
              placeholder="Ex: UTFPR"
              {...form.register("instituicao_origem")}
              error={form.formState.errors.instituicao_origem?.message}
            />
            <Input
              label="Curso"
              placeholder="Ex: Engenharia de Software"
              {...form.register("curso")}
              error={form.formState.errors.curso?.message}
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
            Cadastrar Tutor
          </Button>
        </div>
      </form>
    </div>
  );
}
