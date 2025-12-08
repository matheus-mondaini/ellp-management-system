import { test, expect } from '@playwright/test';

const DOC_LINK_SELECTOR = /Ver documento/;

test.beforeEach(async ({ request }) => {
  await request.post('/api/mock/__reset');
});

test('home page highlights planning documents', async ({ page }) => {
  await page.goto('/');

  await expect(
    page.getByRole('heading', { level: 1, name: 'ELLP Management System' })
  ).toBeVisible();
  await expect(page.getByText('Portal administrativo', { exact: false })).toBeVisible();

  const cards = page.getByRole('article');
  await expect(cards).toHaveCount(3);
  const docLinks = page.getByRole('link', { name: DOC_LINK_SELECTOR });
  await expect(docLinks).toHaveCount(3);
  await expect(docLinks.first()).toHaveAttribute('href', /requirements\.md$/);
});
