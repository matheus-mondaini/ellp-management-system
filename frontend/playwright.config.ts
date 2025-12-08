import { defineConfig, devices } from '@playwright/test';

const PLAYWRIGHT_PORT = parseInt(process.env.PLAYWRIGHT_PORT ?? '3100', 10);
const BASE_URL = `http://127.0.0.1:${PLAYWRIGHT_PORT}`;
const MOCK_API_URL = process.env.NEXT_PUBLIC_API_URL ?? `${BASE_URL}/api/mock`;

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,
  expect: {
    timeout: 10_000,
  },
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev -- --hostname 127.0.0.1',
    port: PLAYWRIGHT_PORT,
    timeout: 120_000,
    reuseExistingServer: !process.env.CI,
    env: {
      PORT: String(PLAYWRIGHT_PORT),
      NEXT_PUBLIC_API_URL: MOCK_API_URL,
    },
  },
});
