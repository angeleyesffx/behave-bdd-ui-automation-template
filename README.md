# Python Behave — BDD UI Automation Framework

[![CI](https://github.com/angeleyesffx/behave-bdd-ui-automation-template/actions/workflows/tests.yml/badge.svg)](https://github.com/angeleyesffx/behave-bdd-ui-automation-template/actions/workflows/tests.yml)

A template for browser and API test automation using [Behave](https://behave.readthedocs.io/en/latest/) (Python BDD), Selenium 4, and the Page Object Model pattern.

---

## Requirements

- Python 3.12+
- pip (updated)

---

## Setup

**Step 1 — Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate        # macOS / Linux
env\Scripts\activate           # Windows
```

**Step 2 — Install dependencies**

```bash
pip install -r requirements.txt
```

> Selenium 4.6+ includes **Selenium Manager**, which downloads the correct browser driver automatically. No manual ChromeDriver/GeckoDriver installation is required.

**Step 3 — Configure environment variables**

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```dotenv
APP_USER=your_app_username
APP_PASSWORD=your_app_password
BASE_URL=https://your-app.com/api
SOME_API_USER=some_user
SOME_API_PASSWORD=some_password
WHATEVER_API_USER=whatever_user
WHATEVER_API_PASSWORD=whatever_password
```

Non-sensitive config (URLs per environment) lives in [features/config.yml](features/config.yml).

---

## Running Tests

**Run the full suite**

```bash
python -m behave
```

**Run without output capture (useful for debugging)**

```bash
python -m behave --no-capture
```

**Run a specific feature file**

```bash
python -m behave features/search.feature
```

**Run by tag**

```bash
# Smoke tests only
python -m behave --tags=@smoke

# All negative scenarios
python -m behave --tags=@negative

# A specific test case
python -m behave --tags=@TC-S001

# Only UI tests, excluding login
python -m behave --tags="@ui and not @feature-login"
```

**Re-run only failed scenarios from the last run**

```bash
python -m behave @rerun.txt
```

---

## Options

**Change browser** (default: `chrome`)

| Value | Browser |
|---|---|
| `chrome` | Google Chrome |
| `headless-chrome` | Chrome headless (no UI, for CI) |
| `firefox` | Mozilla Firefox |
| `edge` | Microsoft Edge |

```bash
python -m behave -D browser=headless-chrome
```

**Change environment** (default: `homolog`)

```bash
python -m behave -D environment=desenv
```

**Combine options**

```bash
python -m behave --no-capture -D environment=desenv -D browser=headless-chrome --tags=@smoke
```

---

## Tag Strategy

Tags follow an ISTQB-aligned traceability model. Every scenario carries:

| Tag | Purpose | Example |
|---|---|---|
| `@ui` / `@api` | Test type | `@ui` |
| `@feature-*` | Feature group | `@feature-search` |
| `@smoke` | Fast regression | `@smoke` |
| `@negative` | Negative/error path | `@negative` |
| `@TC-xxx` | Traceability ID | `@TC-S001` |

Current test cases:

| ID | Feature | Type |
|---|---|---|
| `@TC-S001` | Search returns relevant results | smoke |
| `@TC-S002` | Search navigates away from home page | negative |
| `@TC-L001` | Login with valid credentials | smoke |
| `@TC-L002` | Login with invalid credentials shows error | negative |
| `@TC-A001` | API authentication returns home data | smoke |
| `@TC-A002` | API with invalid credentials returns 401 | negative |

---

## Project Structure

```
.github/
  workflows/
    tests.yml       # CI pipeline (smoke on push, full suite on dispatch)
features/
  pages/            # Page Object classes (BasePage + one class per page)
  steps/            # Step definitions (one file per feature/domain)
  config.yml        # Environment URLs (no credentials)
  datapool.py       # In-memory test data (credentials from env vars)
  environment.py    # Behave hooks (before/after scenario, driver setup)
  object.py         # Page object factory (Singleton per scenario)
.env.example        # Template for required environment variables
behave.ini          # Default Behave configuration
```

---

## Reports

Test reports are written to `build/behave.reports/` after each run:

- **JUnit XML** — for CI integration (Jenkins, GitHub Actions, etc.)
- **Progress report** — `progress3_report.txt`
- **Rerun file** — `rerun.txt` (re-execute only failed scenarios)

Screenshots on failure are saved to `features/screenshots/`.

---

## CI/CD

The GitHub Actions workflow at [.github/workflows/tests.yml](.github/workflows/tests.yml) defines two jobs:

| Job | Trigger | Scope | Secrets required |
|---|---|---|---|
| `smoke-ui` | push / pull request | `@feature-search` | No |
| `full-suite` | `workflow_dispatch` (manual) | tag input (default `@smoke`) | Yes |

To run the full suite manually, go to **Actions → BDD UI Tests → Run workflow** and enter the desired tags (e.g. `@smoke`, `@feature-login`, `@feature-auth`).

Configure the following secrets in your repository settings before triggering `full-suite`:
`APP_USER`, `APP_PASSWORD`, `BASE_URL`, `SOME_API_USER`, `SOME_API_PASSWORD`, `WHATEVER_API_USER`, `WHATEVER_API_PASSWORD`.

---

## References

- [Behave documentation](https://behave.readthedocs.io/en/latest/)
- [Selenium documentation](https://www.selenium.dev/documentation/)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
