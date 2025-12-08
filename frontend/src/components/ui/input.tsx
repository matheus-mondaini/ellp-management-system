"use client";

import { forwardRef, InputHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  helperText?: string;
  error?: string | null;
};

export const Input = forwardRef<HTMLInputElement, Props>(
  ({ className, label, helperText, error, id, ...props }, ref) => {
    return (
      <label className="space-y-1">
        {label && (
          <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            {label}
          </span>
        )}
        <input
          ref={ref}
          id={id}
          className={cn(
            "w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100",
            error && "border-rose-300 focus:border-rose-400 focus:ring-rose-100",
            className,
          )}
          {...props}
        />
        {(helperText || error) && (
          <span className={cn("block text-xs", error ? "text-rose-500" : "text-slate-500")}>{
            error ?? helperText
          }</span>
        )}
      </label>
    );
  },
);

Input.displayName = "Input";
