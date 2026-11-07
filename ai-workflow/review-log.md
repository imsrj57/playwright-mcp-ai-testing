# Review log: AI first draft vs final tests

Comparing [the first draft](ai-drafts/test_checkout_first_draft.py) with the reviewed
[tests/test_checkout.py](../tests/test_checkout.py). The draft ran and passed, which is
exactly why reviewing it matters: most of these problems don't show up as failures.

| # | Problem in the AI draft | Why it matters | What I changed |
|---|---|---|---|
| 1 | `time.sleep(2)` after actions | Slows every run and still flakes on a slow day | Removed. Playwright's `expect()` waits for the condition automatically |
| 2 | Weak assertion: `assert "$" in total` | Passes even if the total is completely wrong | Compare the overview total with the sum of the prices on the products page |
| 3 | `page.is_visible("text=Thank you")` | `is_visible` checks once without waiting, and a partial text match hides wording changes | `expect(...).to_have_text("Thank you for your order!")` plus a URL check |
| 4 | Error test only checks an error *exists* | A wrong error message, or the wrong field failing, would still pass | Parametrised test for each empty field with the exact expected message |
| 5 | Mixed locators: ids, CSS classes, text | Class names change with styling; harder to maintain | One strategy: `get_by_test_id()` on saucedemo's `data-test` attributes |
| 6 | Login and navigation copied into every test | One UI change breaks every test | Page objects in `pages/` and an `inventory` fixture for the logged-in state |
| 7 | Hard-coded full URL | Can't point the suite at another environment | `base_url` in `pytest.ini`, so tests use relative paths |
| 8 | No check that the right item reached the cart | Checkout could pass with an empty or wrong cart | `expect(cart.items).to_have_count(...)` before checking out |

## Takeaway

The agent saved most of the typing and found every element and error message correctly.
What it got wrong was judgement: what to assert, how to wait, and how to keep the suite
maintainable. That part stays with the tester.
