# SEO Redirect & Parity Inventory (V2 Migration)

Last Updated: 2026-04-06 12:00:00

## 1. Global API Strategy

**Locked API Namespace**: `/api/v1/*`
All frontend calls and backend routes must use the `/api/v1` prefix.

| Old API Route | New API Route | Status | Compatibility |
| :--- | :--- | :--- | :--- |
| `/v1/ocr/upload` | `/api/v1/ocr/upload` | Valid | Redirect 301 |
| `/api/upload` | `/api/v1/ocr/upload` | Deprecated | Proxy (30-day) |
| `/api/status/:id` | `/api/v1/ocr/jobs/:id` | Deprecated | Proxy (30-day) |

## 2. Core Redirect Inventory (Hand-Audited)

*Note: Tools (180+) and Blog (15+) are handled via 1:1 parity within their Dynamic Routes.*

| Original Path | New Target Path | Status Code | Parity Status | Parity Tested | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/` | `/` | 200 (OK) | **Matched** | Yes | Root Homepage rebuild |
| `/about` | `/about` | 200 (OK) | **Matched** | No | 1:1 Parity |
| `/about-ocr` | `/about` | 301 (Perm) | **Redirect** | No | Consolidation |
| `/contact` | `/contact` | 200 (OK) | **Missing** | No | Needs Lead Form |
| `/faqs` | `/faqs` | 200 (OK) | **Missing** | No | 1:1 Parity |
| `/mission` | `/about#mission` | 301 (Perm) | **Redirect** | No | Anchor redirect |
| `/privacy` | `/privacy` | 200 (OK) | **Missing** | No | 1:1 Parity |
| `/terms` | `/terms` | 200 (OK) | **Missing** | No | 1:1 Parity |
| `/services` | `/services` | 200 (OK) | **Missing** | No | 1:1 Parity |
| `/tools/image-to-text` | `/tools/image-to-text` | 200 (OK) | **Matched** | No | High-priority Tool |
| `/tools/pdf-to-text` | `/tools/pdf-to-text` | 200 (OK) | **Matched** | No | High-priority Tool |
| `/tools/excel-to-image` | `/tools/excel-to-image` | 200 (OK) | **Planned** | No | Dynamic Group |
| `/tools/word-to-pdf` | `/tools/word-to-pdf` | 200 (OK) | **Planned** | No | Dynamic Group |
| `...` | `...` | `...` | `...` | `...` | (180+ Tools following pattern) |
| `/hire-expert-ai-engineers/uae` | `/hire-expert-ai-engineers/uae` | 200 (OK) | **Planned** | No | **Preserved Keywords** |
| `/hire-expert-ai-engineers/usa` | `/hire-expert-ai-engineers/usa` | 200 (OK) | **Planned** | No | **Preserved Keywords** |
| `/hire-expert-ai-engineers/india` | `/hire-expert-ai-engineers/india` | 200 (OK) | **Planned** | No | **Preserved Keywords** |
| `...` | `...` | `...` | `...` | `...` | (10+ Hires following pattern) |
| `/blog/image-to-text` | `/blog/image-to-text` | 200 (OK) | **Planned** | No | 1:1 Parity |
| `/blog/cost-to-hire-ai-engineers-in-2026-usa-vs-india-vs-europe-vs-dubai` | `/blog/cost-to-hire-ai-engineers-in-2026-usa-vs-india-vs-europe-vs-dubai` | 200 (OK) | **Planned** | No | 1:1 Parity |

## 3. SEO Compliance Table

| Feature | Compliance Policy | Implemented Status |
| :--- | :--- | :--- |
| **Robots (Staging)** | `X-Robots-Tag: noindex, nofollow, noarchive` for `/V2/*`. | **Done** |
| **Canonical (Pre-Parity)** | Omit entirely. | **Done (Layout default)** |
| **Canonical (Post-Parity)** | Set via `generateMetadata` in page component. | **Ready (Template set)** |

## 4. Final Cutover Verification Process

1. **Stage A**: Verify 0% 404s via internal link crawler.
2. **Stage B**: Confirm 1:1 Title/Meta/H1 parity for 10 "Sample Group" Pages.
3. **Stage C**: Execute 301 Redirect Smoke Tests for Legacy Paths.
