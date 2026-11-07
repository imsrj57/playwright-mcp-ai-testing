# Prompts used with Playwright MCP

These are the prompts I give an AI coding agent (Claude Code or GitHub Copilot agent mode)
with the Playwright MCP server connected. Playwright MCP lets the agent open a real browser,
click through the app and read the page's accessibility tree, so it can see actual elements
instead of guessing selectors.

## 1. Explore the app

> Use the Playwright browser to open https://www.saucedemo.com and log in with
> standard_user / secret_sauce. Walk through the main flows: product list, sorting,
> adding and removing items from the cart, and checkout through to the confirmation page.
> List every page you visit, the key elements on each page with their data-test attribute,
> and any validation or error messages you see. Don't write any code yet.

Why: exploring first gives a map of the app and its real locators. Asking for `data-test`
attributes up front steers the agent away from brittle CSS and XPath selectors.

## 2. Find the edge cases

> Now try the negative paths: log in with locked_out_user, with a wrong password, and with
> empty fields. In checkout, submit the form with each field empty in turn. Record the exact
> error message for each case.

Why: the agent is good at trying many inputs quickly. The exact error text becomes the
expected value in the tests.

## 3. Generate tests

> Using what you found, write Python tests with pytest-playwright for the checkout flow.
> Follow the existing page objects in pages/ and the fixtures in tests/conftest.py.
> Use get_by_test_id() locators and Playwright's expect() assertions. No hard-coded waits.

Why: pointing the agent at the existing page objects and conventions keeps generated code
consistent with the framework instead of producing a one-off script.

## 4. Self-heal a broken locator

> This test fails because a locator no longer matches. Open the page with the Playwright
> browser, find the element that the test is trying to reach, and suggest the new locator.
> Explain what changed. Don't change the assertion.

Why: the agent checks the live page instead of guessing. The rule about not touching the
assertion stops it from "fixing" a failing test by weakening what it checks.

## What I always check before merging AI output

See [review-log.md](review-log.md) for the issues found in a real first draft and how each
was fixed. Every generated test is reviewed and run before it goes into the suite.
