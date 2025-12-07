import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "ELLP Management System",
  description: "Portal administrativo do projeto ELLP",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <div className="min-h-screen bg-slate-50">
          <header className="border-b bg-white">
            <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
              <span className="text-lg font-semibold tracking-tight text-slate-900">
                ELLP Management
              </span>
              <span className="text-xs uppercase text-slate-500">Planejamento</span>
            </div>
          </header>
          <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
