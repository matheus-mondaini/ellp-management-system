"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type Tema } from "@/types/api";

export default function TemasPage() {
  const api = useApi();
  const queryClient = useQueryClient();
  const [formOpen, setFormOpen] = useState(false);
  const [editingTema, setEditingTema] = useState<Tema | null>(null);
  const [formData, setFormData] = useState({ nome: "", descricao: "" });
  const [error, setError] = useState<string | null>(null);

  const { data: temas, isLoading } = useQuery({
    queryKey: ["temas"],
    queryFn: () => api<Tema[]>("/temas"),
  });

  const createMutation = useMutation({
    mutationFn: (data: { nome: string; descricao: string }) =>
      api("/temas", { method: "POST", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["temas"] });
      setFormOpen(false);
      setFormData({ nome: "", descricao: "" });
      setError(null);
    },
    onError: (err: Error) => setError(err.message),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: { nome: string; descricao: string } }) =>
      api(`/temas/${id}`, { method: "PATCH", data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["temas"] });
      setEditingTema(null);
      setFormData({ nome: "", descricao: "" });
      setError(null);
    },
    onError: (err: Error) => setError(err.message),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api(`/temas/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["temas"] });
    },
    onError: (err: Error) => alert(err.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.nome || !formData.descricao) {
      setError("Preencha todos os campos");
      return;
    }

    if (editingTema) {
      updateMutation.mutate({ id: editingTema.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleEdit = (tema: Tema) => {
    setEditingTema(tema);
    setFormData({ nome: tema.nome, descricao: tema.descricao || "" });
    setFormOpen(true);
  };

  const handleCancel = () => {
    setFormOpen(false);
    setEditingTema(null);
    setFormData({ nome: "", descricao: "" });
    setError(null);
  };

  return (
    <div className="space-y-8">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-010</p>
          <h1 className="text-3xl font-semibold text-white">Temas das Oficinas</h1>
          <p className="text-sm text-slate-300">
            Categorias para organizar as oficinas (ex: Scratch, Robótica, Arduino).
          </p>
        </div>
        <Button onClick={() => setFormOpen(true)} disabled={formOpen}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Tema
        </Button>
      </header>

      {(formOpen || editingTema) && (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
          <h3 className="mb-4 font-semibold text-white">
            {editingTema ? "Editar Tema" : "Novo Tema"}
          </h3>
          {error && (
            <div className="mb-4 rounded-xl border border-rose-500/40 bg-rose-500/10 p-3 text-sm text-rose-100">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Nome do tema"
              placeholder="Ex: Scratch Básico"
              value={formData.nome}
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
            />
            <div>
              <label htmlFor="tema-descricao" className="block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">
                Descrição
              </label>
              <textarea
                id="tema-descricao"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                placeholder="Descreva o tema e seu objetivo pedagógico..."
                rows={3}
                className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 placeholder:text-slate-400"
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="ghost" onClick={handleCancel}>
                Cancelar
              </Button>
              <Button
                type="submit"
                loading={createMutation.isPending || updateMutation.isPending}
              >
                {editingTema ? "Atualizar" : "Criar"}
              </Button>
            </div>
          </form>
        </div>
      )}

      {isLoading ? (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {temas?.map((tema) => (
            <div
              key={tema.id}
              className="rounded-2xl border border-white/10 bg-white/5 p-6 space-y-3"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-white">{tema.nome}</h3>
                  <p className="text-sm text-slate-400">{tema.descricao}</p>
                </div>
                <Badge className={tema.ativo ? "bg-emerald-500/20 text-emerald-100" : "bg-slate-600/30 text-slate-300"}>
                  {tema.ativo ? "Ativo" : "Inativo"}
                </Badge>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  onClick={() => handleEdit(tema)}
                  disabled={deleteMutation.isPending}
                >
                  <Pencil className="mr-2 h-4 w-4" />
                  Editar
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => {
                    if (confirm(`Deletar tema "${tema.nome}"?`)) {
                      deleteMutation.mutate(tema.id);
                    }
                  }}
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Deletar
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {!isLoading && temas?.length === 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-12 text-center">
          <p className="text-slate-400">Nenhum tema cadastrado ainda.</p>
        </div>
      )}
    </div>
  );
}
