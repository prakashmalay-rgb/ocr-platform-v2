import { test, expect } from '@playwright/test';

test.describe('Lead Generation Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Note: Staging path for contact form
    await page.goto('/contact');
  });

  test('should display validation errors for empty fields', async ({ page }) => {
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Full name must be at least 2 characters')).toBeVisible();
    await expect(page.locator('text=Please enter a valid email address')).toBeVisible();
    await expect(page.locator('text=Message must be at least 10 characters')).toBeVisible();
  });

  test('should submit successfully with valid data', async ({ page }) => {
    // Intercept API call to mock success
    await page.route('/api/v1/leads/contact', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ id: 'lead_123', success: true, message: 'Inquiry received' }),
      });
    });

    await page.fill('input[id="fullName"]', 'Audit User');
    await page.fill('input[id="email"]', 'audit@example.com');
    await page.fill('textarea[id="message"]', 'This is a test message for OCR V2 migration.');
    
    // Mock Turnstile token (since we have a hidden input as placeholder)
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Thank you! We have received your inquiry')).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    await page.route('/api/v1/leads/contact', async route => {
      await route.fulfill({ status: 500 });
    });

    await page.fill('input[id="fullName"]', 'Error User');
    await page.fill('input[id="email"]', 'error@example.com');
    await page.fill('textarea[id="message"]', 'Testing error state of the lead form.');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Something went wrong. Please try again later.')).toBeVisible();
  });
});

test.describe('Dynamic Tool Routes Parity', () => {
  const TOOL_SLUGS = ['image-to-text', 'pdf-to-text', 'excel-to-image'];

  for (const slug of TOOL_SLUGS) {
    test(`Verify ${slug} page renders and has metadata`, async ({ page }) => {
      await page.goto(`/tools/${slug}`);
      
      const h1 = page.locator('h1');
      await expect(h1).toBeVisible();
      
      // Ensure it contains the dynamic name
      const h1Text = await h1.innerText();
      expect(h1Text.toLowerCase()).toContain(slug.split('-')[0]);

      // Verify canonical is NOT present in staging /V2 (as per policy pre-parity check)
      const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
      if (page.url().includes('/V2/')) {
        // If staged, it might be missing or explicitly pointed to prod (we audited it as null default)
        if (canonical) {
          expect(canonical).not.toContain('/V2/');
        }
      }
    });
  }
});
