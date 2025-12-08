"use client";

import { motion } from "framer-motion";

export function PresenceTrend() {
  const percentages = [68, 72, 78, 84, 81, 86];

  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-white">
      <header className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-400">Presença Média</p>
          <h3 className="text-lg font-semibold">Semanas recentes</h3>
        </div>
        <span className="text-sm text-emerald-300">+8% vs mês anterior</span>
      </header>

      <div className="mt-6 grid grid-cols-6 gap-3">
        {percentages.map((percent, index) => (
          <div key={index} className="flex flex-col items-center gap-2">
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: `${percent}%` }}
              transition={{ delay: index * 0.1 }}
              className="w-full max-w-[24px] rounded-full bg-gradient-to-t from-emerald-500/20 to-emerald-400"
              style={{ minHeight: 20 }}
            />
            <span className="text-xs text-slate-400">{percent}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
