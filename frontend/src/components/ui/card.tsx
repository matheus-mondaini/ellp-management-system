"use client";

import { type ReactNode } from "react";

import { cn } from "@/lib/utils";

export function Card({
  title,
  description,
  children,
  className,
  footer,
}: {
  title?: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
  footer?: ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-lg shadow-slate-900/5", className)}>
      {(title || description) && (
        <header className="space-y-1">
          {typeof title === "string" ? (
            <h2 className="text-base font-semibold text-slate-900">{title}</h2>
          ) : (
            title
          )}
          {description && <p className="text-sm text-slate-500">{description}</p>}
        </header>
      )}
      {children && <div className={cn((title || description) && "mt-4")}>{children}</div>}
      {footer && <div className="mt-4 border-t border-slate-100 pt-4 text-sm text-slate-500">{footer}</div>}
    </section>
  );
}
