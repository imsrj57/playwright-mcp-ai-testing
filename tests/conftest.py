import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# Public demo credentials published on saucedemo.com itself.
PASSWORD = "secret_sauce"
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"


@pytest.fixture(scope="session", autouse=True)
def use_data_test_attribute(playwright):
    """Saucedemo uses data-test="..." instead of Playwright's default data-testid."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def inventory(page) -> InventoryPage:
    """A logged-in session, starting on the products page."""
    LoginPage(page).open().login(STANDARD_USER, PASSWORD)
    return InventoryPage(page)
