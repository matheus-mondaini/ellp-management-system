"use client";

import { forwardRef, SelectHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type Props = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string;
  helperText?: string;
  error?: string | null;
};

export const Select = forwardRef<HTMLSelectElement, Props>(
  ({ className, label, helperText, error, children, ...props }, ref) => {
    return (
      <label className="space-y-1">
        {label && (
          <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            {label}
          </span>
        )}
        <div className="relative">
          <select
            ref={ref}
            className={cn(
              "w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100",
              error && "border-rose-300 focus:border-rose-400 focus:ring-rose-100",
              className,
            )}
            {...props}
          >
            {children}
          </select>
          <span className="pointer-events-none absolute inset-y-0 right-4 flex items-center text-slate-400">▾</span>
        </div>
        {(helperText || error) && (
          <span className={cn("block text-xs", error ? "text-rose-500" : "text-slate-500")}>{
            error ?? helperText
          }</span>
        )}
      </label>
    );
  },
);

Select.displayName = "Select";
