"use client";

import { useAuthStore } from "@/lib/auth-store";

export function AuthHeader() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-white">
      <div className="rounded-full bg-emerald-400/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.3em] text-emerald-200">
        {user?.role ?? "???"}
      </div>
      <div>
        <p className="font-semibold">{user?.nome_completo ?? "Operador"}</p>
        <p className="text-xs text-slate-300">{user?.email ?? "—"}</p>
      </div>
    </div>
  );
}
