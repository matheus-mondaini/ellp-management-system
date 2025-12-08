import { env } from "./env";

export class ApiError extends Error {
  status: number;
  payload: unknown;

  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}

export type ApiRequestOptions = {
  method?: string;
  token?: string | null;
  data?: unknown;
  searchParams?: Record<string, string | number | undefined | null>;
  headers?: HeadersInit;
};

const buildUrl = (path: string, searchParams?: ApiRequestOptions["searchParams"]) => {
  const base = env.apiUrl.replace(/\/$/, "");
  const url = new URL(path.startsWith("/") ? `${base}${path}` : `${base}/${path}`);
  if (searchParams) {
    Object.entries(searchParams).forEach(([key, value]) => {
      if (value === undefined || value === null) return;
      url.searchParams.set(key, String(value));
    });
  }
  return url;
};

export async function apiFetch<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const { method = "GET", token, data, headers, searchParams } = options;
  const url = buildUrl(path, searchParams);
  const computedHeaders = new Headers(headers);
  computedHeaders.set("Accept", "application/json");

  let body: BodyInit | undefined;
  if (data instanceof FormData) {
    body = data;
  } else if (data !== undefined) {
    computedHeaders.set("Content-Type", "application/json");
    body = JSON.stringify(data);
  }

  if (token) {
    computedHeaders.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(url, {
    method,
    headers: computedHeaders,
    body,
    cache: "no-store",
  });

  const contentType = response.headers.get("content-type");
  const payload = contentType?.includes("application/json") ? await response.json() : await response.text();

  if (!response.ok) {
    throw new ApiError(
      (payload as { detail?: string })?.detail || `API request failed with status ${response.status}`,
      response.status,
      payload,
    );
  }

  return payload as T;
}
