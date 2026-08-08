import { defineConfig, devices } from '@playwright/test';

const chromiumExecutable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['junit', { outputFile: 'reports/playwright-junit.xml' }]
  ],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    launchOptions: chromiumExecutable ? { executablePath: chromiumExecutable } : undefined,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'python -m uvicorn llm_quality_harness.api:app --host 127.0.0.1 --port 8000',
    url: 'http://127.0.0.1:8000/health',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
    env: {
      ...process.env,
      LLMQ_PROJECT_ROOT: process.cwd(),
      LLMQ_STORE_PATH: 'reports/e2e-results.db'
    }
  }
});
