import { type ClassValue, clsx } from "clsx";

export const cn = (...inputs: ClassValue[]) => clsx(inputs);

export const formatPercent = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return "–";
  return `${value.toFixed(1)}%`;
};

export const titleCase = (value: string) =>
  value
    .split(/[-_\s]/)
    .filter(Boolean)
    .map((chunk) => chunk.at(0)?.toUpperCase() + chunk.slice(1))
    .join(" ");
