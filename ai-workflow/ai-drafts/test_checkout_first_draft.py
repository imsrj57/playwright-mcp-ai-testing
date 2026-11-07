# FIRST DRAFT, kept for comparison. Not part of the test suite (pytest only collects tests/).
#
# This is the kind of code an AI agent produces on a first pass before review.
# It runs, but it has the problems listed in ../review-log.md.
# The reviewed version is tests/test_checkout.py.

import time


def test_checkout(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    time.sleep(2)

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")
    time.sleep(1)
    page.click("#checkout")

    page.fill("#first-name", "John")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "12345")
    page.click("#continue")
    time.sleep(1)

    total = page.inner_text(".summary_subtotal_label")
    assert "$" in total

    page.click("#finish")
    assert page.is_visible("text=Thank you")


def test_checkout_errors(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")
    page.click("#checkout")
    page.click("#continue")
    assert page.is_visible("[data-test='error']")
