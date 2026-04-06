---
description: How to run Playwright tests locally and in CI
---

# Playwright Testing Workflow

This workflow ensures that all UI, SEO, and functional tests pass before code is pushed to the `main` branch.

## 1. Local Execution
Before pushing any changes, run the full test suite locally.

// turbo
```powershell
# Navigate to frontend app
cd apps/frontend

# Install dependencies if not already present
npm install

# Run all Playwright tests
npx playwright test
```

## 2. Running Specific Tests
To run only SEO or specific feature tests:

```powershell
# Run only SEO tests
npx playwright test tests/seo.spec.ts

# Run tests in headed mode (UI visible)
npx playwright test --headed
```

## 3. Reviewing Reports
If tests fail, a report is generated automatically.

```powershell
npx playwright show-report
```

## 4. CI/CD Integration
The `main` branch is protected. All Pull Requests to `main` must pass the Playwright suite in GitHub Actions.

### Release Checklist
- [ ] All tests pass locally.
- [ ] No regression in SEO metadata (Title/Meta/Canonical).
- [ ] "White Layered" design consistency verified.
- [ ] OCR upload flow functional on Staging.
- [ ] Mobile responsiveness verified.
