"use client";

import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";

import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { type CreateOficinaPayload, type Oficina, type Tema } from "@/types/api";
import { useApi } from "@/hooks/use-api";
import { cn } from "@/lib/utils";

const schema = z.object({
  titulo: z.string().min(3),
  descricao: z.string().optional(),
  objetivo: z.string().optional(),
  carga_horaria: z.number().min(1),
  capacidade_maxima: z.number().min(1),
  numero_aulas: z.number().min(1).nullable().optional(),
  data_inicio: z.string(),
  data_fim: z.string(),
  local: z.string(),
  dias_semana: z.string().optional(),
  horario: z.string().optional(),
  professor_id: z.string().uuid(),
  tema_ids: z.array(z.string().uuid()).default([]),
});

type FormValues = z.infer<typeof schema>;

export function OficinaForm({ onCreated, className }: { onCreated: (oficina: Oficina) => void; className?: string }) {
  const api = useApi();
  const { data: temas } = useQuery({ queryKey: ["temas"], queryFn: () => api<Tema[]>("/temas") });

  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      carga_horaria: 8,
      capacidade_maxima: 15,
      data_inicio: new Date().toISOString().slice(0, 10),
      data_fim: new Date().toISOString().slice(0, 10),
      tema_ids: [],
    },
  });

  const mutation = useMutation({
    mutationFn: (payload: CreateOficinaPayload) => api<Oficina>("/oficinas", { method: "POST", data: payload }),
    onSuccess: (created) => {
      onCreated(created);
    },
  });

  const onSubmit = (values: FormValues) => {
    mutation.mutate({ ...values });
    form.reset();
  };

  const temaOptions = useMemo(() => temas ?? [], [temas]);

  return (
    <form className={cn("grid gap-4", className)} onSubmit={form.handleSubmit(onSubmit)}>
      <Input label="Título" {...form.register("titulo")} error={form.formState.errors.titulo?.message} />
      <Textarea label="Descrição" rows={3} {...form.register("descricao")} />
      <Textarea label="Objetivo" rows={3} {...form.register("objetivo")} />
      <div className="grid gap-4 md:grid-cols-3">
        <Input type="number" label="Carga horária" {...form.register("carga_horaria", { valueAsNumber: true })} />
        <Input type="number" label="Capacidade" {...form.register("capacidade_maxima", { valueAsNumber: true })} />
        <Input type="number" label="Número de aulas" {...form.register("numero_aulas", { valueAsNumber: true })} />
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <Input type="date" label="Data início" {...form.register("data_inicio")} />
        <Input type="date" label="Data fim" {...form.register("data_fim")} />
      </div>
      <Input label="Local" {...form.register("local")} />
      <Input label="Dias da semana" {...form.register("dias_semana")} />
      <Input label="Horário" {...form.register("horario")} />
      <Input label="Professor ID" {...form.register("professor_id")} error={form.formState.errors.professor_id?.message} />
      <Select
        multiple
        label="Temas"
        value={form.watch("tema_ids")}
        onChange={(event) => {
          const selection = Array.from(event.target.selectedOptions).map((option) => option.value);
          form.setValue("tema_ids", selection);
        }}
      >
        {temaOptions.map((tema) => (
          <option key={tema.id} value={tema.id}>
            {tema.nome}
          </option>
        ))}
      </Select>
      <Button type="submit" loading={mutation.isPending} disabled={mutation.isPending}>
        {mutation.isPending ? "Salvando…" : "Salvar oficina"}
      </Button>
    </form>
  );
}
