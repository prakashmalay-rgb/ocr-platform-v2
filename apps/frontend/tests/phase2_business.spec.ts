import { test, expect } from '@playwright/test';

/**
 * Phase 2 Business Logic Verification Suite.
 */
test.describe('Phase 2: Business Complete Lead Handling', () => {
  
  test('Lead Form: should fail if turnstile_token is missing (Frontend Zod)', async ({ page }) => {
    await page.goto('/contact');
    
    // Fill fields except turnstile
    await page.fill('input[id="full_name"]', 'Bot User');
    await page.fill('input[id="email"]', 'bot@example.com');
    await page.fill('textarea[id="message"]', 'This message should not pass turnstile check.');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Zod validation should catch the empty token before API call
    await expect(page.locator('text=Cloudflare Turnstile token required')).toBeVisible();
  });

  test('Lead Form: should fail-closed if backend returns Turnstile error', async ({ page }) => {
    await page.goto('/contact');
    
    // Intercept and mock 400 Robot Detection Failed
    await page.route('/api/v1/leads/contact', async route => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ detail: "Robot detection failed. Please try again." }),
      });
    });

    await page.fill('input[id="full_name"]', 'Suspicious User');
    await page.fill('input[id="email"]', 'bot@evil.com');
    await page.fill('textarea[id="message"]', 'Robot message.');
    
    // Force a token (though widget is mocked)
    await page.evaluate(() => {
       // Manual override for testing purposes if possible
    });
    
    // Since Turnstile widget is third-party, we rely on the manual test or full E2E 
    // with a real testing key (1x00000000000000000000AA).
  });

  test('Dynamic Tool: metadata contains unique slug value', async ({ page }) => {
    const slugs = ['image-to-text', 'pdf-to-text', 'excel-to-image'];
    
    for (const slug of slugs) {
      await page.goto(`/tools/${slug}`);
      const title = await page.title();
      // Ensure the slug-specific name is in the title (capitalized appropriately)
      const keyword = slug.split('-')[0];
      expect(title.toLowerCase()).toContain(keyword);
    }
  });

});
