import { test, expect } from '@playwright/test';

test('certificate validation page echoes hash parameter', async ({ page }) => {
  const hash = 'pw-e2e-hash';
  await page.goto(`/validar/${hash}`);

  await expect(
    page.getByRole('heading', { level: 1, name: /Validação de Certificado/ })
  ).toBeVisible();
  await expect(page.getByText('Hash consultado', { exact: false })).toContainText(hash);
  await expect(page.getByText('endpoint público', { exact: false })).toBeVisible();
});
