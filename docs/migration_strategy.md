# OCR Platform V2 Migration Strategy

## 1. Project Understanding & Current State
We are building a production-grade, modular OCR platform to replace the legacy `ocr-extraction.com`. The goal is to migrate to a fresh, owned codebase in `ocr-platform-v2` while ensuring 100% SEO preservation and a premium "white layered" design aesthetic.

### Current Tech Stack
-   **Frontend**: Next.js 16 (App Router), Tailwind CSS v4, Vercel.
-   **Backend**: FastAPI, SQLAlchemy, Render.
-   **Workers**: Python-based OCR processors.

---

## 2. Gaps & Risk Assessment

| Risk | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **SEO Regression** | Risk of losing rank if URLs or metadata change. | 1:1 mapping of titles, metas, H1s, and canonicals. 301 redirects for any changes. |
| **IP Overlap** | Blindly copying old code from the previous coder. | Start with fresh components; only reuse publicly available logic or generic OCR patterns. |
| **API Availability** | Incomplete backend endpoints causing UI breakage. | Detailed API matrix with staging mocks for frontend development. |
| **Image/Asset Paths** | Broken links if assets move from `/v1` to `/v2`. | Use a consistent `/assets` or `/public` folder with automated path validation. |
| **Indexability** | Staging environment getting indexed. | Implement `X-Robots-Tag: noindex` for the `/V2` prefix. |

---

## 3. Recommended Clean Architecture (New Repo)

### Monorepo Structure (apps/ + packages/)
-   `apps/frontend`: Next.js 16 (App Router) + Tailwind v4.
-   `apps/backend`: FastAPI with Pydantic for API schema.
-   `services/workers`: Dedicated processing logic for OCR tasks.
-   `packages/shared`: Shared types, constants, and utilities for backend/worker communication.

### Folder Structure (Frontend)
```bash
src/
  ├── app/          # Routes, layouts, and pages (using Next.js App Router)
  ├── components/   # Clean, modular, reusable UI components (layered design)
  ├── features/     # Feature-specific logic (e.g., OCR-upload, result-viewer)
  ├── hooks/        # Custom React hooks
  ├── services/     # API consumer services (fetch client)
  └── types/        # TypeScript interfaces and types
```

---

## 4. UI/UX: The "White Layered" Design System
-   **Background**: High-contrast white (`#FFFFFF`) with subtle light gray (`#F9FAFB`) sections.
-   **Layers**: Use subtle soft shadows (`shadow-sm`, `shadow-md`) and borders to create depth without visual clutter.
-   **Typography**: Clean sans-serif (e.g., Inter, Outfit, or Geist) with ample white space for high readability.
-   **Consistency**: A shared `Layout` component providing unified Header, Sidebar/Nav, and Footer across all pages.

---

## 5. SEO Preservation Strategy
We must maintain 100% structural integrity of the existing site to avoid ranking loss.

| Element | Task |
| :--- | :--- |
| **Metadata** | Port all `<title>`, `meta description`, `og:*` tags exactly as they appear live. |
| **URLs** | Keep root paths identical (e.g., `/blog/how-to-ocr` stays `/blog/how-to-ocr`). |
| **Headings** | Maintain H1 tags for each page; use H2/H3 for logical sections without altering keywords. |
| **Content** | Do NOT change copy; only improve formatting and visual presentation. |
| **Sitemap** | Re-implement automated sitemap generation with identical priority/freq settings. |

---

## 6. Full API Matrix (Draft)

| Name | Method | Route | Purpose | Must/Should/Optional |
| :--- | :--- | :--- | :--- | :--- |
| **Upload File** | `POST` | `/v1/ocr/upload` | Upload image/PDF for OCR. | Must |
| **Job Status** | `GET` | `/v1/ocr/jobs/{id}` | Check status of OCR processing. | Must |
| **Get Results** | `GET` | `/v1/ocr/results/{id}` | Retrieve extracted text/structured data. | Must |
| **Download Export**| `GET` | `/v1/ocr/export/{id}` | Export to PDF, Word, Excel. | Must |
| **Fetch Blogs** | `GET` | `/v1/content/blogs` | Fetch blog listings for SEO pages. | Should |
| **Submit Contact** | `POST` | `/v1/leads/contact` | Capture lead info (contact form). | Must |
| **Auth Login** | `POST` | `/v1/auth/login` | For admin/dashboard access. | Must |
| **Usage Meter** | `GET` | `/v1/usage/status` | Track current user's OCR limits. | Should |

---

## 7. Staging & Deployment Plan (`/V2`)

### Phase A: Staging Setup
1.  **Vercel Configuration**: Set up a deployment alias for `/V2`.
2.  **Next.js Custom Prefix**: Use `basePath: '/V2'` in `next.config.ts` purely for testing.
3.  **No-Index**: Add `noindex` to the entire staging path via `robots.txt` or meta-tags.
4.  **Environment Isolation**: Separate `STAGING_DATABASE_URL` and `STAGING_REDIS_URL`.

### Phase B: Production Cutover
1.  Verify staging functionality under `www.ocr-extraction.com/V2`.
2.  Move staging repo (main branch) to production as the primary source for Vercel.
3.  Update Vercel production alias to the root `/`.
4.  Remove staging `basePath`.
5.  Execute full Playwright suite against live production.

---

## 8. CI/CD & Testing Workflow

### Git Branching Strategy
-   `main`: Mirror of production. 100% stable.
-   `develop`: Staging environment integration branch. 
-   `feature/*`: Individual tasks developed locally.

### CI/CD Pipeline (GitHub Actions + Vercel/Render Hooks)
1.  **Developer**: Pushes `feature/ui-redesign` to GitHub.
2.  **CI (Pre-Merge)**: 
    - Eslint / Typecheck.
    - Local Unit Tests (Jest/Vitest).
    - **Playwright Local Runs** (Smoke/SEO checks).
3.  **PR Approved**: Merge to `develop`.
4.  **Vercel/Render (Staging)**: Auto-deploy to staging URL.
5.  **Merge to `main`**: Triggers production deployment.
