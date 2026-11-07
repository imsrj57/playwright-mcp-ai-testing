import re

import pytest
from playwright.sync_api import expect

from pages.checkout_page import CartPage, CheckoutPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def add_items_and_start_checkout(inventory, page, *products):
    for product in products:
        inventory.add_to_cart(product)
    inventory.go_to_cart()
    cart = CartPage(page)
    expect(cart.items).to_have_count(len(products))
    cart.checkout()
    return CheckoutPage(page)


@pytest.mark.smoke
def test_complete_purchase(inventory, page):
    checkout = add_items_and_start_checkout(inventory, page, BACKPACK)

    checkout.fill_details("Suraj", "Nair", "411001")
    checkout.finish()

    expect(page).to_have_url(re.compile(r"/checkout\-complete\.html$"))
    expect(checkout.complete_header).to_have_text("Thank you for your order!")


def test_item_total_matches_product_prices(inventory, page):
    """The overview total must equal the sum of the prices shown on the products page."""
    inventory.sort_by("az")
    names = inventory.item_names.all_inner_texts()
    prices = dict(zip(names, inventory.prices()))
    expected_total = round(prices[BACKPACK] + prices[BIKE_LIGHT], 2)

    checkout = add_items_and_start_checkout(inventory, page, BACKPACK, BIKE_LIGHT)
    checkout.fill_details("Suraj", "Nair", "411001")

    assert checkout.item_total() == pytest.approx(expected_total)


@pytest.mark.parametrize(
    "first, last, postal, message",
    [
        pytest.param("", "Nair", "411001", "Error: First Name is required", id="missing-first-name"),
        pytest.param("Suraj", "", "411001", "Error: Last Name is required", id="missing-last-name"),
        pytest.param("Suraj", "Nair", "", "Error: Postal Code is required", id="missing-postal-code"),
    ],
)
def test_checkout_form_validation(inventory, page, first, last, postal, message):
    checkout = add_items_and_start_checkout(inventory, page, BACKPACK)

    checkout.fill_details(first, last, postal)

    expect(checkout.error).to_have_text(message)
    expect(page).to_have_url(re.compile(r"/checkout\-step\-one\.html$"))
