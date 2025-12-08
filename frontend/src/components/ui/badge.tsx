"use client";

import { type ReactNode } from "react";

import { cn } from "@/lib/utils";

const variants = {
  default: "bg-slate-900 text-white",
  success: "bg-emerald-100 text-emerald-700",
  warning: "bg-amber-100 text-amber-600",
  info: "bg-sky-100 text-sky-700",
  danger: "bg-rose-100 text-rose-600",
};

type Variant = keyof typeof variants;

export function Badge({ children, variant = "default", className }: { children: ReactNode; variant?: Variant; className?: string }) {
  return (
    <span className={cn("inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide", variants[variant], className)}>
      {children}
    </span>
  );
}
