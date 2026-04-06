import { test, expect } from '@playwright/test';

test.describe('SEO Metadata Parity Checks', () => {
  test('homepage has correct metadata', async ({ page }) => {
    await page.goto('/');

    // Check Title
    await expect(page).toHaveTitle(/Free OCR to Text | Convert Image to Text & Excel | 100% Accurate/i);

    // Check Meta Description
    const description = await page.getAttribute('meta[name="description"]', 'content');
    expect(description).toContain('Global AI platform specializing in AI workflow orchestration');

    // Check H1 Tag
    const h1 = await page.locator('h1').innerText();
    expect(h1).toBe('Free OCR To Text Converter');
  });

  test('about page has correct metadata', async ({ page }) => {
    await page.goto('/about');

    await expect(page).toHaveTitle(/About Us - OCR Extraction/i);
    await expect(page.locator('h1')).toHaveText('About Us');
  });

  test('canonical tags are correct', async ({ page }) => {
    await page.goto('/');
    const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
    // Ensure it points to the production root, not the staging /V2 (optional but best practice)
    expect(canonical).toBe('https://www.ocr-extraction.com/');
  });
});
