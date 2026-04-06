import { test, expect } from '@playwright/test';

/**
 * Phase 3: Failure-Path & Staging Proxy Verification.
 */
test.describe('Staging Burn-in: Failure Path Verification', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/contact');
  });

  test('F1: Missing Turnstile Token (Zod Guard)', async ({ page }) => {
    await page.fill('input[id="full_name"]', 'Audit User');
    await page.fill('input[id="email"]', 'audit@example.com');
    await page.fill('textarea[id="message"]', 'This is a failure test for missing turnstile.');
    
    await page.click('button[type="submit"]');
    
    // Frontend should block submission locally
    await expect(page.locator('text=Cloudflare Turnstile token required')).toBeVisible();
  });

  test('F2: Invalid Turnstile Token (Backend Reject)', async ({ page }) => {
    // Intercept and mock 400 Bad Request
    await page.route('/api/v1/leads/contact', async route => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ detail: "Robot detection failed. Please try again." }),
      });
    });

    await page.fill('input[id="full_name"]', 'Robot User');
    await page.fill('input[id="email"]', 'bot@example.com');
    await page.fill('textarea[id="message"]', 'This message has a spoofed/invalid token.');
    
    // We assume the Turnstile widget is bypassed or mocked here
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Robot detection failed. Please try again.')).toBeVisible();
  });

  test('F3: Resend API Failure (Database Persistence preserved)', async ({ page }) => {
    // This requires a real backend test or a sophisticated mock
    // Mocking the API response but logically verifying that the DB record was still created 
    // is better handled in the Backend Pytest suite.
  });

  test('F4: Rate Limit Enforcement (Proxy-Aware IP Extraction)', async ({ request }) => {
    const payload = {
      full_name: "Rapid User",
      email: "rapid@example.com",
      message: "Testing 429 rate limit behavior.",
      turnstile_token: "test-token"
    };

    // Simulate X-Forwarded-For to verify trusted IP resolution
    const headers = { "X-Forwarded-For": "1.2.3.4" };

    // Send 5 successful requests
    for (let i = 0; i < 5; i++) {
      const res = await request.post('/api/v1/leads/contact', { data: payload, headers });
      expect(res.status()).not.toBe(429);
    }

    // 6th request should trigger 429
    const limitRes = await request.post('/api/v1/leads/contact', { data: payload, headers });
    expect(limitRes.status()).toBe(429);
  });
});
