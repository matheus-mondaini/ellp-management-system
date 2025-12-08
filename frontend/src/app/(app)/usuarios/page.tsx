"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Shield, ShieldCheck, Users2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type UserRole, type UserSummary } from "@/types/api";

const roleLabels: Record<UserRole, string> = {
  admin: "Admin",
  professor: "Professor",
  tutor: "Tutor",
  aluno: "Aluno",
};

const roleColors: Record<UserRole, string> = {
  admin: "bg-rose-500/20 text-rose-100",
  professor: "bg-sky-500/20 text-sky-100",
  tutor: "bg-emerald-500/20 text-emerald-100",
  aluno: "bg-white/10 text-white",
};

export default function UsuariosPage() {
  const api = useApi();
  const [roleFilter, setRoleFilter] = useState<UserRole | "todos">("todos");
  const [onlyActive, setOnlyActive] = useState(true);

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["usuarios"],
    queryFn: () => api<UserSummary[]>("/users"),
  });

  const filtered = useMemo(() => {
    if (!data) return [];
    return data.filter((user) => {
      const roleMatch = roleFilter === "todos" || user.role === roleFilter;
      const activeMatch = !onlyActive || user.ativo;
      return roleMatch && activeMatch;
    });
  }, [data, roleFilter, onlyActive]);

  return (
    <div className="space-y-8">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Governança</p>
          <h1 className="text-3xl font-semibold text-white">Usuários e perfis</h1>
          <p className="text-sm text-slate-300">Controle de permissões alinhado ao backend FastAPI.</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => window.location.href = "/usuarios/alunos/criar"}>
            + Aluno
          </Button>
          <Button onClick={() => window.location.href = "/usuarios/professores/criar"}>
            + Professor
          </Button>
          <Button onClick={() => window.location.href = "/usuarios/tutores/criar"}>
            + Tutor
          </Button>
        </div>
      </header>

      <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-white">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-slate-400">
            <Users2 className="h-4 w-4" /> Filtros rápidos
          </div>
          <div className="flex flex-wrap gap-2">
            {(["todos", "admin", "professor", "tutor", "aluno"] as Array<UserRole | "todos">).map((role) => (
              <button
                key={role}
                type="button"
                onClick={() => setRoleFilter(role)}
                className={`rounded-full border px-4 py-1 text-xs font-semibold uppercase tracking-[0.3em] transition ${
                  roleFilter === role
                    ? "border-white bg-white/20 text-white"
                    : "border-white/20 text-white/60 hover:text-white"
                }`}
              >
                {role === "todos" ? "Todos" : roleLabels[role]}
              </button>
            ))}
          </div>
          <label className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-slate-400">
            <input
              type="checkbox"
              checked={onlyActive}
              onChange={(event) => setOnlyActive(event.target.checked)}
              className="h-4 w-4 rounded border-white/40 bg-transparent text-emerald-400 focus:ring-emerald-400"
            />
            Somente ativos
          </label>
        </div>

        {isError && (
          <div className="mt-4 rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-100">
            Falha ao carregar usuários: {(error as Error)?.message ?? "erro inesperado"}
          </div>
        )}

        <div className="mt-6 overflow-hidden rounded-2xl border border-white/10">
          <table className="w-full table-auto text-left text-sm">
            <thead className="bg-white/5 text-xs uppercase tracking-[0.3em] text-slate-400">
              <tr>
                <th className="px-4 py-3 font-medium">Usuário</th>
                <th className="px-4 py-3 font-medium">E-mail</th>
                <th className="px-4 py-3 font-medium">Perfil</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {isLoading && (
                <tr>
                  <td colSpan={4} className="px-4 py-8">
                    <Skeleton className="h-10 w-full bg-white/10" />
                  </td>
                </tr>
              )}
              {!isLoading && filtered.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-4 py-8 text-center text-slate-400">
                    Nenhum usuário para os filtros selecionados.
                  </td>
                </tr>
              )}
              {filtered.map((user) => (
                <tr key={user.id} className="border-t border-white/5">
                  <td className="px-4 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-lg font-semibold text-white">
                        {user.nome_completo.slice(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <p className="font-semibold text-white">{user.nome_completo}</p>
                        <p className="text-xs text-slate-400">ID: {user.id.slice(0, 8)}…</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4 text-slate-200">{user.email}</td>
                  <td className="px-4 py-4">
                    <Badge className={roleColors[user.role]}>{roleLabels[user.role]}</Badge>
                  </td>
                  <td className="px-4 py-4">
                    {user.ativo ? (
                      <span className="inline-flex items-center gap-2 text-sm text-emerald-200">
                        <ShieldCheck className="h-4 w-4" /> Ativo
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-2 text-sm text-rose-200">
                        <Shield className="h-4 w-4" /> Suspenso
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
