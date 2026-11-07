from pages.base_page import BasePage


def product_slug(name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack', the format saucedemo uses in its test ids."""
    return name.lower().replace(" ", "-")


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def title(self):
        return self.by_test_id("title")

    @property
    def item_names(self):
        return self.by_test_id("inventory-item-name")

    @property
    def item_prices(self):
        return self.by_test_id("inventory-item-price")

    @property
    def cart_badge(self):
        return self.by_test_id("shopping-cart-badge")

    def add_to_cart(self, product_name: str):
        self.by_test_id(f"add-to-cart-{product_slug(product_name)}").click()

    def remove_from_cart(self, product_name: str):
        self.by_test_id(f"remove-{product_slug(product_name)}").click()

    def sort_by(self, option: str):
        """option is one of: az, za, lohi, hilo"""
        self.by_test_id("product-sort-container").select_option(option)

    def prices(self) -> list[float]:
        return [float(text.replace("$", "")) for text in self.item_prices.all_inner_texts()]

    def go_to_cart(self):
        self.by_test_id("shopping-cart-link").click()
