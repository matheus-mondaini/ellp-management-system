"use client";

import { CalendarDays, IdCard, LayoutDashboard, Users2 } from "lucide-react";

import { NavLink } from "./nav-link";

const links = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/oficinas", label: "Oficinas", icon: CalendarDays },
  { href: "/certificados", label: "Certificados", icon: IdCard },
  { href: "/usuarios", label: "Usuários", icon: Users2 },
];

export function Sidebar() {
  return (
    <aside className="relative flex flex-col gap-6 rounded-[2.5rem] bg-slate-900/95 p-6 text-white shadow-[0_20px_60px_rgba(15,23,42,0.35)]">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-emerald-300">ELLP</p>
        <p className="text-xl font-semibold leading-tight">Management</p>
        <p className="text-sm text-slate-400">Operação das oficinas extensionistas</p>
      </div>
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink key={link.href} {...link} />
        ))}
      </nav>
      <div className="mt-auto rounded-3xl bg-gradient-to-br from-emerald-400/20 to-sky-400/20 p-4 text-sm text-slate-200">
        <p className="font-semibold text-white">Sprint atual</p>
        <p className="text-xs text-slate-300">Foco: certificados & presença</p>
        <p className="mt-1 text-2xl font-black text-white">Semana 2</p>
      </div>
    </aside>
  );
}
