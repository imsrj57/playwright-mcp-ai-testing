import re

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from tests.conftest import LOCKED_OUT_USER, PASSWORD, STANDARD_USER


@pytest.mark.smoke
def test_valid_user_lands_on_products_page(login_page, page):
    login_page.login(STANDARD_USER, PASSWORD)

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, message",
    [
        pytest.param(LOCKED_OUT_USER, PASSWORD,
                     "Epic sadface: Sorry, this user has been locked out.", id="locked-out-user"),
        pytest.param(STANDARD_USER, "wrong_password",
                     "Epic sadface: Username and password do not match any user in this service",
                     id="wrong-password"),
        pytest.param("", PASSWORD, "Epic sadface: Username is required", id="missing-username"),
        pytest.param(STANDARD_USER, "", "Epic sadface: Password is required", id="missing-password"),
    ],
)
def test_login_errors(login_page, page, username, password, message):
    login_page.login(username, password)

    expect(login_page.error).to_have_text(message)
    expect(page).not_to_have_url(re.compile(r"/inventory\.html$"))
