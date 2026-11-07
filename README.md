# Playwright + MCP: AI-Assisted Test Automation

![Playwright tests](https://github.com/imsrj57/playwright-mcp-ai-testing/actions/workflows/playwright.yml/badge.svg)

A Python Playwright framework for [saucedemo.com](https://www.saucedemo.com), built with an
AI agent connected to the **Playwright MCP server**, and reviewed by hand before anything
went into the suite.

The point of this repo isn't "AI wrote my tests". It shows where AI actually speeds up test
automation (exploring the app, finding locators, drafting code) and where a tester still has
to step in (what to assert, how to wait, how to keep the suite maintainable). The
[review log](ai-workflow/review-log.md) shows that side by side.

## What's covered

15 tests across the main flows:

| Area | Tests |
|---|---|
| Login | valid login, locked-out user, wrong password, missing username, missing password |
| Products | all 6 products shown, sort by price both ways, sort by name, cart badge count on add and remove |
| Checkout | full purchase end to end, item total matches product prices, form validation for each required field |

## The AI workflow

1. **Explore.** The agent opens the site through Playwright MCP, walks through every flow and
   lists the pages, elements (with their `data-test` attributes) and error messages.
2. **Find edge cases.** It tries the negative paths and records the exact error text.
3. **Generate.** It drafts tests that follow the existing page objects and fixtures.
4. **Review.** I review every draft before it goes in. See what changed in
   [review-log.md](ai-workflow/review-log.md): it removed sleeps, made assertions stronger,
   moved to one locator strategy and used page objects.
5. **Self-heal.** When a locator breaks, the agent checks the live page and suggests a fix,
   without being allowed to weaken the assertion.

The exact prompts are in [ai-workflow/prompts.md](ai-workflow/prompts.md), and the raw first
draft is kept in [ai-workflow/ai-drafts/](ai-workflow/ai-drafts/) for comparison.

### Connect Playwright MCP yourself

The repo already includes the config for both tools:

- **Claude Code** reads [`.mcp.json`](.mcp.json) when you open the folder.
- **VS Code / GitHub Copilot agent mode** reads [`.vscode/mcp.json`](.vscode/mcp.json).

Both start the server with `npx @playwright/mcp@latest`, so you need Node.js installed.

## Run the tests

```bash
pip install -r requirements.txt
python -m playwright install chromium

pytest                      # all tests
pytest -m smoke             # quick smoke set
pytest -n auto              # in parallel
pytest --headed             # watch the browser
pytest --html=reports/report.html --self-contained-html
```

CI runs the full suite in parallel on every push, keeping a trace and a screenshot for any
failure, and uploads the HTML report as an artifact.

## Structure

```
pages/                  page objects: login, inventory, cart and checkout
tests/
  conftest.py           fixtures, logged-in session, data-test locator setup
  test_login.py  test_inventory.py  test_checkout.py
ai-workflow/
  prompts.md            prompts used with the Playwright MCP agent
  review-log.md         what the AI draft got wrong and how it was fixed
  ai-drafts/            the raw first draft, not part of the suite
.mcp.json               Playwright MCP config for Claude Code
.vscode/mcp.json        Playwright MCP config for VS Code / Copilot
```

### Design choices

- **One locator strategy.** Saucedemo puts a `data-test` attribute on its elements, so
  `conftest.py` registers it as Playwright's test id and every locator is `get_by_test_id()`.
- **No sleeps.** Every check uses Playwright's `expect()`, which waits for the condition.
- **Check values, not just presence.** The checkout total is compared with real product
  prices, and error tests check the exact message for each field.

## Author

Suraj Nair, SDET · [LinkedIn](https://www.linkedin.com/in/imsrj)
