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

const alunoSchema = z.object({
  nome_completo: z.string().min(3, "Nome deve ter no mínimo 3 caracteres"),
  email: z.string().email("E-mail inválido"),
  senha: z.string().min(8, "Senha deve ter no mínimo 8 caracteres"),
  telefone: z.string().optional(),
  data_nascimento: z.string(),
  responsavel_nome: z.string().min(3, "Nome do responsável obrigatório"),
  responsavel_email: z.string().email("E-mail do responsável inválido"),
  responsavel_telefone: z.string().min(10, "Telefone do responsável obrigatório"),
});

type AlunoFormData = z.infer<typeof alunoSchema>;

export default function CriarAlunoPage() {
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<AlunoFormData>({
    resolver: zodResolver(alunoSchema),
  });

  const mutation = useMutation({
    mutationFn: (data: AlunoFormData) => api("/users/alunos", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
      router.push("/usuarios");
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const onSubmit = (data: AlunoFormData) => {
    setError(null);
    mutation.mutate(data);
  };

  return (
    <div className="space-y-8">
      <div>
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="mb-4 text-slate-300 hover:text-white text-sm"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-001</p>
        <h1 className="text-3xl font-semibold text-white">Cadastrar Aluno</h1>
        <p className="text-sm text-slate-300">
          Cadastro de aluno (criança) com dados do responsável.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
          {error}
        </div>
      )}

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="rounded-2xl bg-white/5 p-6 space-y-4">
          <h3 className="font-semibold text-white">Dados do Aluno</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <Input
              label="Nome completo"
              {...form.register("nome_completo")}
              error={form.formState.errors.nome_completo?.message}
            />
            <Input
              label="Data de nascimento"
              type="date"
              {...form.register("data_nascimento")}
              error={form.formState.errors.data_nascimento?.message}
            />
            <Input
              label="E-mail (opcional)"
              type="email"
              {...form.register("email")}
              error={form.formState.errors.email?.message}
            />
            <Input
              label="Telefone (opcional)"
              {...form.register("telefone")}
              error={form.formState.errors.telefone?.message}
            />
            <Input
              label="Senha inicial"
              type="password"
              {...form.register("senha")}
              error={form.formState.errors.senha?.message}
            />
          </div>
        </div>

        <div className="rounded-2xl bg-white/5 p-6 space-y-4">
          <h3 className="font-semibold text-white">Dados do Responsável</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <Input
              label="Nome do responsável"
              {...form.register("responsavel_nome")}
              error={form.formState.errors.responsavel_nome?.message}
            />
            <Input
              label="E-mail do responsável"
              type="email"
              {...form.register("responsavel_email")}
              error={form.formState.errors.responsavel_email?.message}
            />
            <Input
              label="Telefone do responsável"
              {...form.register("responsavel_telefone")}
              error={form.formState.errors.responsavel_telefone?.message}
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
            Cadastrar Aluno
          </Button>
        </div>
      </form>
    </div>
  );
}
