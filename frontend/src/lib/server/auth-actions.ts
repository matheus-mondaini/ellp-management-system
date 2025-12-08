"use server";

import { cookies } from "next/headers";

export async function getServerToken() {
  const cookieStore = await cookies();
  const token = cookieStore.get("accessToken")?.value || process.env.NEXT_PUBLIC_API_TOKEN;
  return token ?? null;
}
