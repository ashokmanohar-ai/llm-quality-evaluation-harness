import { expect, test } from '@playwright/test';

test('runs the governed reference suite and renders evidence', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Turn model behavior/ })).toBeVisible();

  await page.getByRole('button', { name: 'Run reference suite' }).click();

  await expect(page.getByText('Evidence captured')).toBeVisible();
  await expect(page.getByText('Release gate passed')).toBeVisible();
  await expect(page.locator('#suite-score')).toHaveText('100%');
  await expect(page.locator('#case-results tr')).toHaveCount(8);
  await expect(page.locator('.status.failed')).toHaveCount(0);
});

test('exposes health, metadata, and deterministic demo APIs', async ({ request }) => {
  const health = await request.get('/health');
  expect(health.ok()).toBeTruthy();
  expect(await health.json()).toMatchObject({ status: 'healthy' });

  const info = await request.get('/api/info');
  expect(info.ok()).toBeTruthy();
  expect(await info.json()).toMatchObject({ offline_baseline: true });

  const demo = await request.post('/api/demo');
  expect(demo.ok()).toBeTruthy();
  const result = await demo.json();
  expect(result.summary.failed_cases).toBe(0);
  expect(result.summary.safety_case_pass_rate).toBe(1);
});

