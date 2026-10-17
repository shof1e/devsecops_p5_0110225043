"""Unit test untuk modul inventory, validators, dan report."""

import pytest

from app.inventory import Inventory
from app.report import generate_summary
from app.validators import is_valid_price, is_valid_quantity, is_valid_sku


def test_add_item_new():
    inv = Inventory()
    item = inv.add_item("BRG-00101", "Kabel HDMI", 10, 45000)
    assert item.quantity == 10
    assert inv.get_item("BRG-00101") is not None


def test_add_item_merge_existing_stock():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 10, 45000)
    inv.add_item("BRG-00101", "Kabel HDMI", 5, 45000)
    assert inv.get_item("BRG-00101").quantity == 15


def test_remove_stock_success():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 10, 45000)
    inv.remove_stock("BRG-00101", 4)
    assert inv.get_item("BRG-00101").quantity == 6


def test_remove_stock_insufficient_raises():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 2, 45000)
    with pytest.raises(ValueError):
        inv.remove_stock("BRG-00101", 5)


def test_remove_stock_unknown_sku_raises():
    inv = Inventory()
    with pytest.raises(KeyError):
        inv.remove_stock("TIDAK-ADA", 1)


def test_low_stock_items():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 2, 45000)
    inv.add_item("BRG-00102", "Mouse", 20, 120000)
    low = inv.low_stock_items(threshold=5)
    assert len(low) == 1
    assert low[0].sku == "BRG-00101"


def test_generate_summary():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 2, 45000)
    summary = generate_summary(inv, low_stock_threshold=5)
    assert summary["total_sku"] == 1
    assert summary["low_stock_count"] == 1


@pytest.mark.parametrize(
    "sku,expected",
    [
        ("BRG-00123", True),
        ("brg-00123", False),
        ("BRG-1", False),
        (123, False),
    ],
)
def test_is_valid_sku(sku, expected):
    assert is_valid_sku(sku) is expected


def test_is_valid_quantity():
    assert is_valid_quantity(5) is True
    assert is_valid_quantity(-1) is False
    assert is_valid_quantity(1.5) is False


def test_is_valid_price():
    assert is_valid_price(1000) is True
    assert is_valid_price(-10) is False
