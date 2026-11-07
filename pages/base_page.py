from playwright.sync_api import Page


class BasePage:
    """Shared helpers. Saucedemo marks elements with data-test attributes, which
    conftest.py registers as Playwright's test id, so get_by_test_id() finds them."""

    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.path)
        return self

    def by_test_id(self, test_id: str):
        return self.page.get_by_test_id(test_id)
