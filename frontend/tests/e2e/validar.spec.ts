import { test, expect } from '@playwright/test';

test.beforeEach(async ({ request }) => {
  await request.post('/api/mock/__reset');
});

test('certificate validation page renders mock API data', async ({ page, request }) => {
  const response = await request.get('/api/mock/certificados');
  const certificates = (await response.json()) as Array<{ hash_validacao: string }>;
  const hash = certificates[0]?.hash_validacao ?? 'ellp-hash-demo';

  await page.goto(`/validar/${hash}`);

  await expect(
    page.getByRole('heading', { level: 1, name: 'Resultado da validação' })
  ).toBeVisible();
  await expect(page.getByText(/Certificado válido/)).toBeVisible();
  await expect(page.getByText(/Ana Clara Souza/)).toBeVisible();
  await expect(page.getByRole('link', { name: /Baixar PDF/ })).toHaveAttribute('href', /storage\.ellp\.dev/);
});
