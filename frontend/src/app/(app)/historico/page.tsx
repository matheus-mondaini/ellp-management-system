"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Award } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import { type UserSummary } from "@/types/api";

interface HistoricoItem {
  id: string;
  oficina_titulo: string;
  oficina_periodo: string;
  status: string;
  percentual_presenca: number;
  certificado_emitido: boolean;
}

export default function HistoricoPage() {
  const api = useApi();
  const [userId, setUserId] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const { data: usuarios } = useQuery({
    queryKey: ["usuarios"],
    queryFn: () => api<UserSummary[]>("/users"),
  });

  const { data: historico, isLoading, refetch } = useQuery({
    queryKey: ["historico", userId],
    queryFn: () => api<HistoricoItem[]>(`/users/${userId}/historico`),
    enabled: false,
  });

  const filteredUsuarios = usuarios?.filter((u) =>
    u.nome_completo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSearch = (id: string) => {
    setUserId(id);
    refetch();
  };

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">RF-013</p>
        <h1 className="text-3xl font-semibold text-white">Histórico de Participação</h1>
        <p className="text-sm text-slate-300">
          Consulte o histórico completo de oficinas por aluno, tutor ou professor.
        </p>
      </div>

      <div className="rounded-2xl bg-white/5 p-6 space-y-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <Input
              label="Buscar usuário"
              placeholder="Digite o nome..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {searchTerm && filteredUsuarios && (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {filteredUsuarios.map((usuario) => (
              <button
                key={usuario.id}
                type="button"
                onClick={() => handleSearch(usuario.id)}
                className="w-full rounded-xl border border-white/10 bg-white/5 p-4 text-left transition hover:bg-white/10"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-white">{usuario.nome_completo}</p>
                    <p className="text-sm text-slate-400">{usuario.email}</p>
                  </div>
                  <Badge>{usuario.role}</Badge>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {isLoading && (
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      )}

      {historico && historico.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white">Oficinas Participadas</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {historico.map((item) => (
              <div
                key={item.id}
                className="rounded-2xl border border-white/10 bg-white/5 p-6 space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-white">{item.oficina_titulo}</h3>
                    <p className="text-sm text-slate-400">{item.oficina_periodo}</p>
                  </div>
                  <Badge>{item.status}</Badge>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-slate-400">Presença</p>
                    <p className="text-white font-semibold">{item.percentual_presenca}%</p>
                  </div>
                  {item.certificado_emitido && (
                    <div>
                      <Award className="h-4 w-4 text-emerald-400 mb-1" />
                      <p className="text-emerald-400 text-xs">Certificado emitido</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {historico && historico.length === 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-12 text-center">
          <p className="text-slate-400">Nenhum histórico encontrado para este usuário.</p>
        </div>
      )}
    </div>
  );
}
