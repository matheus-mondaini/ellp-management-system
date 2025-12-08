import { test, expect, type Page } from '@playwright/test';

const ADMIN_EMAIL = 'admin@ellp.test';
const ADMIN_PASSWORD = 'admin12345';

async function login(page: Page) {
  await page.goto('/login');
  await page.getByLabel('E-mail institucional').fill(ADMIN_EMAIL);
  await page.getByLabel('Senha').fill(ADMIN_PASSWORD);
  await page.getByRole('button', { name: /Entrar/i }).click();
  await page.waitForURL('**/dashboard');
}

test.beforeEach(async ({ request }) => {
  await request.post('/api/mock/__reset');
});

test('admin consegue autenticar e visualizar métricas do dashboard', async ({ page }) => {
  await login(page);

  await expect(page.getByRole('heading', { level: 1, name: 'Dashboard operacional' })).toBeVisible();
  await expect(page.getByText('Oficinas ativas')).toBeVisible();
  await expect(page.getByText('Inscrições totais')).toBeVisible();
  await expect(page.getByText(/Conclusão das inscrições/)).toBeVisible();

  const metricValue = page.getByText('Certificados emitidos').locator('xpath=../following-sibling::*[1]');
  await expect(metricValue).toContainText(/\d+/);
});

test('listagem de oficinas reflete criação através do formulário', async ({ page, request }) => {
  await login(page);

  await page.getByRole('link', { name: 'Oficinas' }).click();
  await expect(page).toHaveURL('**/oficinas');

  const usersResponse = await request.get('/api/mock/users');
  const users = (await usersResponse.json()) as Array<{ id: string; role: string }>;
  const professorId = users.find((user) => user.role === 'professor')?.id ?? '00000000-0000-0000-0000-000000000000';

  await page.getByRole('button', { name: /Nova oficina/i }).click();
  await page.getByLabel('Título').fill('Oficina Playwright E2E');
  await page.getByLabel('Descrição').fill('Fluxo criado nos testes automatizados');
  await page.getByLabel('Carga horária').fill('10');
  await page.getByLabel('Capacidade').fill('15');
  await page.getByLabel('Número de aulas').fill('5');
  await page.getByLabel('Data início').fill('2025-01-10');
  await page.getByLabel('Data fim').fill('2025-01-20');
  await page.getByLabel('Local').fill('UTFPR - Bloco F');
  await page.getByLabel('Professor ID').fill(professorId);
  await page.getByRole('button', { name: /Salvar oficina/i }).click();

  await expect(page.getByRole('cell', { name: 'Oficina Playwright E2E' })).toBeVisible();
});
