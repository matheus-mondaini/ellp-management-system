import type { Metadata } from "next";
import type { ReactNode } from "react";

import "../../styles/globals.css";

export const metadata: Metadata = {
  title: "ELLP — Portal Público",
};

export default function PublicLayout({ children }: { children: ReactNode }) {
  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center px-4 py-12 text-white">
      <div className="max-w-3xl space-y-8 text-center">
        <header className="space-y-2">
          <p className="text-xs uppercase tracking-[0.4em] text-emerald-300">Projeto ELLP</p>
          <h1 className="text-4xl font-semibold">Ensino Lúdico de Lógica e Programação</h1>
          <p className="text-base text-slate-300">
            Portal público para validação de certificados das oficinas extensionistas.
          </p>
        </header>
        <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 backdrop-blur-xl">
          {children}
        </div>
      </div>
    </div>
  );
}
