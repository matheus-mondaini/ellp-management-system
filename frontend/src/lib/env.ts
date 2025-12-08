const getPublicEnv = (key: string, fallback?: string): string => {
  const value = process.env[key];
  if (value === undefined || value === "") {
    if (fallback !== undefined) {
      return fallback;
    }
    throw new Error(`Environment variable ${key} is not defined`);
  }
  return value;
};

export const env = {
  apiUrl: getPublicEnv("NEXT_PUBLIC_API_URL", "http://localhost:8000"),
  supabaseUrl: getPublicEnv("NEXT_PUBLIC_SUPABASE_URL", ""),
  supabaseAnonKey: getPublicEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY", ""),
  supabaseStorageBucket: getPublicEnv("NEXT_PUBLIC_SUPABASE_STORAGE_BUCKET", "certificados"),
};
