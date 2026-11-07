import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_shows_all_six_products(inventory):
    expect(inventory.item_names).to_have_count(6)


def test_sort_price_low_to_high(inventory):
    inventory.sort_by("lohi")

    prices = inventory.prices()
    assert prices == sorted(prices), f"Prices are not ascending: {prices}"


def test_sort_price_high_to_low(inventory):
    inventory.sort_by("hilo")

    prices = inventory.prices()
    assert prices == sorted(prices, reverse=True), f"Prices are not descending: {prices}"


def test_sort_name_z_to_a(inventory):
    inventory.sort_by("za")

    names = inventory.item_names.all_inner_texts()
    assert names == sorted(names, reverse=True), f"Names are not Z to A: {names}"


def test_cart_badge_counts_items(inventory):
    expect(inventory.cart_badge).to_be_hidden()

    inventory.add_to_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")

    inventory.add_to_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_have_text("2")

    inventory.remove_from_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")
