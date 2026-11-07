import re

from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    @property
    def items(self):
        return self.by_test_id("inventory-item")

    def checkout(self):
        self.by_test_id("checkout").click()


class CheckoutPage(BasePage):
    """Covers the three checkout steps: your information, overview and complete."""

    @property
    def error(self):
        return self.by_test_id("error")

    @property
    def complete_header(self):
        return self.by_test_id("complete-header")

    def fill_details(self, first_name: str, last_name: str, postal_code: str):
        self.by_test_id("firstName").fill(first_name)
        self.by_test_id("lastName").fill(last_name)
        self.by_test_id("postalCode").fill(postal_code)
        self.by_test_id("continue").click()

    def item_total(self) -> float:
        """Reads 'Item total: $39.98' from the overview step."""
        text = self.by_test_id("subtotal-label").inner_text()
        return float(re.search(r"[\d.]+", text).group())

    def finish(self):
        self.by_test_id("finish").click()
