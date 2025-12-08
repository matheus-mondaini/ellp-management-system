import type { APIRequestContext } from '@playwright/test';

export async function resetMockApi(request: APIRequestContext) {
  const maxAttempts = 5;
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    try {
      const response = await request.post('/api/mock/reset', {
        failOnStatusCode: false,
        timeout: 10000,
      });
      if (response.ok()) {
        return;
      }
      console.log(`Tentativa ${attempt + 1}: Status ${response.status()}`);
    } catch (error) {
      console.log(`Tentativa ${attempt + 1}: Erro`, error);
      if (attempt === maxAttempts - 1) {
        console.warn('Aviso: Não foi possível resetar o mock API, continuando sem reset');
        return;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 200 * (attempt + 1)));
  }
  console.warn('Aviso: Não foi possível resetar o mock API após múltiplas tentativas');
}
