import type { APIRequestContext } from '@playwright/test';

export async function resetMockApi(request: APIRequestContext) {
  const maxAttempts = 5;
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    try {
      const response = await request.post('/api/mock/__reset', {
        failOnStatusCode: false,
      });
      if (response.ok()) {
        return;
      }
    } catch (error) {
      if (attempt === maxAttempts - 1) {
        throw error;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 200 * (attempt + 1)));
  }
  throw new Error('Não foi possível resetar o mock API');
}
