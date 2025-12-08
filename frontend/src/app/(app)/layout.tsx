import { Suspense, type ReactNode } from "react";

import { AuthGate } from "@/components/auth/auth-gate";
import { AuthHeader } from "@/components/auth/auth-header";
import { LogoutButton } from "@/components/auth/logout-button";
import { Sidebar } from "@/components/layout/sidebar";

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGate>
      <div className="mx-auto flex min-h-screen max-w-7xl gap-10 px-6 py-10">
        <aside className="w-64 shrink-0">
          <Suspense fallback={<div className="text-center text-sm text-white/60">Carregando navegação…</div>}>
            <Sidebar />
          </Suspense>
        </aside>
        <main className="flex-1 space-y-8">
          <header className="flex items-center justify-between gap-4">
            <Suspense fallback={<div className="h-11 w-40 animate-pulse rounded-full bg-white/10" />}>
              <AuthHeader />
            </Suspense>
            <LogoutButton />
          </header>
          <div className="rounded-3xl border border-white/5 bg-slate-900/60 p-8 shadow-xl shadow-slate-950/40">
            {children}
          </div>
        </main>
      </div>
    </AuthGate>
  );
}
