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

const editUsuarioSchema = z.object({
  nome_completo: z.string().min(3, "Nome deve ter pelo menos 3 caracteres"),
  cpf: z.string().regex(/^\d{11}$/, "CPF deve ter 11 dígitos"),
  email: z.string().email("Email inválido"),
  telefone: z.string().regex(/^\d{10,11}$/, "Telefone inválido"),
  endereco_completo: z.string().min(5, "Endereço deve ter pelo menos 5 caracteres"),
  data_nascimento: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida"),
});

type EditUsuarioForm = z.infer<typeof editUsuarioSchema>;

export default function EditarUsuarioPage() {
  const params = useParams();
  const router = useRouter();
  const api = useApi();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const userId = params.id as string;

  const { data: usuario, isLoading } = useQuery({
    queryKey: ["usuario", userId],
    queryFn: () => api<any>(`/users/${userId}`),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EditUsuarioForm>({
    resolver: zodResolver(editUsuarioSchema),
    values: usuario
      ? {
          nome_completo: usuario.nome_completo,
          cpf: usuario.cpf,
          email: usuario.email,
          telefone: usuario.telefone,
          endereco_completo: usuario.endereco_completo,
          data_nascimento: usuario.data_nascimento,
        }
      : undefined,
  });

  const mutation = useMutation({
    mutationFn: (data: EditUsuarioForm) => api(`/users/${userId}`, { method: "PUT", data }),
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Usuário atualizado com sucesso.",
      });
      queryClient.invalidateQueries({ queryKey: ["usuario", userId] });
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
      router.push("/usuarios");
    },
    onError: () => {
      toast({
        title: "Erro",
        description: "Não foi possível atualizar o usuário.",
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

  if (!usuario) {
    return (
      <div className="rounded-2xl border border-white/10 bg-white/5 p-12 text-center">
        <p className="text-slate-400">Usuário não encontrado.</p>
        <Button onClick={() => router.push("/usuarios")} className="mt-4">
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
        <h1 className="text-3xl font-semibold text-white">Editar Usuário</h1>
        <p className="text-sm text-slate-300">
          Atualize as informações de {usuario.nome_completo}.
        </p>
      </div>

      <form
        onSubmit={handleSubmit((data) => mutation.mutate(data))}
        className="rounded-2xl bg-white/5 p-6 space-y-4"
      >
        <Input
          label="Nome Completo"
          {...register("nome_completo")}
          error={errors.nome_completo?.message}
        />
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="CPF (somente números)"
            {...register("cpf")}
            error={errors.cpf?.message}
            maxLength={11}
          />
          <Input
            label="Data de Nascimento"
            type="date"
            {...register("data_nascimento")}
            error={errors.data_nascimento?.message}
          />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Email"
            type="email"
            {...register("email")}
            error={errors.email?.message}
          />
          <Input
            label="Telefone (DDD + número)"
            {...register("telefone")}
            error={errors.telefone?.message}
            maxLength={11}
          />
        </div>
        <Input
          label="Endereço Completo"
          {...register("endereco_completo")}
          error={errors.endereco_completo?.message}
        />
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
