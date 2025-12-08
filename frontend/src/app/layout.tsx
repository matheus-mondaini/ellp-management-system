import type { Metadata } from "next";
import "../styles/globals.css";
import { Providers } from "@/components/providers";

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
    <html lang="pt-BR" suppressHydrationWarning>
      <body className="relative min-h-screen bg-slate-950 text-slate-50">
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute left-1/2 top-20 h-96 w-96 -translate-x-1/2 rounded-full bg-emerald-500/30 blur-[140px]" />
          <div className="absolute right-0 top-0 h-80 w-80 translate-x-1/3 rounded-full bg-sky-500/20 blur-[120px]" />
        </div>
        <Providers>
          <main className="relative z-10 min-h-screen bg-gradient-to-br from-slate-950/90 via-slate-950/60 to-slate-900/80">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
