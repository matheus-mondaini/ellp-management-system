"use client";

import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ArrowLeft, Save } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { useToast } from "@/hooks/use-toast";
import { type UserSummary } from "@/types/api";

const editOficinaSchema = z
  .object({
    titulo: z.string().min(5, "Título deve ter pelo menos 5 caracteres"),
    descricao: z.string().min(10, "Descrição deve ter pelo menos 10 caracteres"),
    data_inicio: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida"),
    data_fim: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida"),
    horario: z.string().regex(/^\d{2}:\d{2}$/, "Horário inválido (HH:MM)"),
    local: z.string().min(3, "Local deve ter pelo menos 3 caracteres"),
    vagas_totais: z.coerce.number().int().positive("Vagas deve ser positivo"),
    professor_id: z.string().uuid("Selecione um professor"),
    tema_id: z.string().uuid("Selecione um tema"),
  })
  .refine((data) => new Date(data.data_fim) >= new Date(data.data_inicio), {
    message: "Data fim deve ser posterior à data início",
    path: ["data_fim"],
  });

type EditOficinaForm = z.infer<typeof editOficinaSchema>;

export default function EditarOficinaPage() {
  const params = useParams();
  const router = useRouter();
  const api = useApi();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const oficinaId = params.id as string;

  const { data: oficina, isLoading } = useQuery({
    queryKey: ["oficina", oficinaId],
    queryFn: () => api<any>(`/oficinas/${oficinaId}`),
  });

  const { data: professores } = useQuery({
    queryKey: ["professores"],
    queryFn: () => api<UserSummary[]>("/users?role=professor"),
  });

  const { data: temas } = useQuery({
    queryKey: ["temas"],
    queryFn: () => api<any[]>("/temas"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EditOficinaForm>({
    resolver: zodResolver(editOficinaSchema),
    values: oficina
      ? {
          titulo: oficina.titulo,
          descricao: oficina.descricao,
          data_inicio: oficina.data_inicio,
          data_fim: oficina.data_fim,
          horario: oficina.horario,
          local: oficina.local,
          vagas_totais: oficina.vagas_totais,
          professor_id: oficina.professor_id,
          tema_id: oficina.tema_id,
        }
      : undefined,
  });

  const mutation = useMutation({
    mutationFn: (data: EditOficinaForm) =>
      api(`/oficinas/${oficinaId}`, { method: "PUT", data }),
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Oficina atualizada com sucesso.",
      });
      queryClient.invalidateQueries({ queryKey: ["oficina", oficinaId] });
      queryClient.invalidateQueries({ queryKey: ["oficinas"] });
      router.push(`/oficinas/${oficinaId}`);
    },
    onError: () => {
      toast({
        title: "Erro",
        description: "Não foi possível atualizar a oficina.",
        variant: "error",
      });
    },
  });

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-8 w-64" />
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      </div>
    );
  }

  if (!oficina) {
    return (
      <div className="rounded-2xl border border-white/10 bg-white/5 p-12 text-center">
        <p className="text-slate-400">Oficina não encontrada.</p>
        <Button onClick={() => router.push("/oficinas")} className="mt-4">
          Voltar
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <Button
          variant="secondary"
          onClick={() => router.back()}
          className="mb-4 gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <h1 className="text-3xl font-semibold text-white">Editar Oficina</h1>
        <p className="text-sm text-slate-300">
          Atualize as informações de {oficina.titulo}.
        </p>
      </div>

      <form
        onSubmit={handleSubmit((data) => mutation.mutate(data))}
        className="rounded-2xl bg-white/5 p-6 space-y-4"
      >
        <Input
          label="Título da Oficina"
          {...register("titulo")}
          error={errors.titulo?.message}
        />
        <div>
          <label htmlFor="oficina-descricao" className="block text-sm font-medium text-slate-300 mb-2">
            Descrição
          </label>
          <textarea
            id="oficina-descricao"
            {...register("descricao")}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400"
            rows={4}
          />
          {errors.descricao && (
            <p className="mt-1 text-xs text-red-400">{errors.descricao.message}</p>
          )}
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Data de Início"
            type="date"
            {...register("data_inicio")}
            error={errors.data_inicio?.message}
          />
          <Input
            label="Data de Fim"
            type="date"
            {...register("data_fim")}
            error={errors.data_fim?.message}
          />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Horário (HH:MM)"
            placeholder="14:00"
            {...register("horario")}
            error={errors.horario?.message}
          />
          <Input
            label="Vagas Totais"
            type="number"
            {...register("vagas_totais")}
            error={errors.vagas_totais?.message}
          />
        </div>
        <Input
          label="Local"
          {...register("local")}
          error={errors.local?.message}
        />
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label htmlFor="oficina-professor" className="block text-sm font-medium text-slate-300 mb-2">
              Professor Responsável
            </label>
            <select
              id="oficina-professor"
              {...register("professor_id")}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400"
            >
              <option value="">Selecione um professor</option>
              {professores?.map((prof) => (
                <option key={prof.id} value={prof.id}>
                  {prof.nome_completo}
                </option>
              ))}
            </select>
            {errors.professor_id && (
              <p className="mt-1 text-xs text-red-400">{errors.professor_id.message}</p>
            )}
          </div>
          <div>
            <label htmlFor="oficina-tema" className="block text-sm font-medium text-slate-300 mb-2">
              Tema
            </label>
            <select
              id="oficina-tema"
              {...register("tema_id")}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400"
            >
              <option value="">Selecione um tema</option>
              {temas?.map((tema) => (
                <option key={tema.id} value={tema.id}>
                  {tema.nome}
                </option>
              ))}
            </select>
            {errors.tema_id && (
              <p className="mt-1 text-xs text-red-400">{errors.tema_id.message}</p>
            )}
          </div>
        </div>
        <div className="flex justify-end gap-2 pt-4">
          <Button
            type="button"
            variant="secondary"
            onClick={() => router.back()}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={mutation.isPending} className="gap-2">
            <Save className="h-4 w-4" />
            {mutation.isPending ? "Salvando..." : "Salvar Alterações"}
          </Button>
        </div>
      </form>
    </div>
  );
}
