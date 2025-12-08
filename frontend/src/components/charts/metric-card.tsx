import { type ReactNode } from "react";

import { cn } from "@/lib/utils";

export function MetricCard({ label, value, trend, icon }: { label: string; value: ReactNode; trend?: string; icon?: ReactNode }) {
  return (
    <div className="rounded-3xl border border-white/5 bg-white/5 p-5 text-white shadow-lg shadow-black/10">
      <div className="flex items-center justify-between text-sm uppercase tracking-[0.4em] text-slate-400">
        <span>{label}</span>
        {icon}
      </div>
      <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
      {trend && <p className="text-sm text-emerald-300">{trend}</p>}
    </div>
  );
}
