import { test, expect } from '@playwright/test';

/**
 * Automated Staging Guard Suite.
 * This test suite ensures the /V2 staging environment is blocked from indexing.
 */
test.describe('Staging SEO Guard Check (/V2)', () => {
  const STAGED_URLS = [
    '/V2/',
    '/V2/about',
    '/V2/tools/image-to-text',
    '/V2/tools/pdf-to-text',
  ];

  for (const url of STAGED_URLS) {
    test(`Verify X-Robots-Tag for ${url}`, async ({ request }) => {
      const response = await request.get(url);
      
      // Ensure the X-Robots-Tag is correctly set to prevent staging indexing
      expect(response.status()).toBe(200);
      expect(response.headers()['x-robots-tag']).toContain('noindex');
      expect(response.headers()['x-robots-tag']).toContain('nofollow');
      expect(response.headers()['x-robots-tag']).toContain('noarchive');
    });

    test(`Verify Canonical points to prod for ${url}`, async ({ page }) => {
      await page.goto(url);
      
      // Extract canonical URL from the head
      const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
      
      if (canonical) {
        // Must point to production root, NOT the staging /V2 path
        expect(canonical).not.toContain('/V2/');
        expect(canonical).toContain('https://www.ocr-extraction.com/');
      }
      
      // Note: If canonical is missing, that is also a valid state for pre-parity as per our policy.
    });
  }
});
