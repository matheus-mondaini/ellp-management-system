"use client";

import { ButtonHTMLAttributes, forwardRef } from "react";

import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "ghost" | "danger";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  loading?: boolean;
};

const styles: Record<Variant, string> = {
  primary:
    "bg-emerald-600 text-white hover:bg-emerald-500 focus-visible:outline-emerald-600",
  secondary:
    "bg-white text-slate-900 ring-1 ring-inset ring-slate-200 hover:bg-slate-50",
  ghost: "text-slate-600 hover:text-slate-900 hover:bg-slate-100/70",
  danger: "bg-rose-600 text-white hover:bg-rose-500 focus-visible:outline-rose-600",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, children, variant = "primary", loading = false, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2",
          styles[variant],
          (disabled || loading) && "cursor-not-allowed opacity-60",
          className,
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <span className="inline-flex h-3 w-3 animate-spin rounded-full border-2 border-white/50 border-t-transparent" />
        )}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";
