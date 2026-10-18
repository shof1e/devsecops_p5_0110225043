"""Unit test untuk modul inventory, validators, report, dan main."""

import pytest

from app.inventory import Inventory
from app.main import run_demo
from app.report import format_summary_text, generate_summary
from app.validators import (
    is_valid_price,
    is_valid_quantity,
    is_valid_sku,
    validate_item_input,
)


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


def test_is_valid_price_rejects_non_numeric():
    assert is_valid_price("murah") is False


def test_validate_item_input_all_valid():
    errors = validate_item_input("BRG-00123", 10, 5000)
    assert errors == []


def test_validate_item_input_all_invalid():
    errors = validate_item_input("salah", -1, -5)
    assert len(errors) == 3


def test_format_summary_text_with_low_stock():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 2, 45000)
    summary = generate_summary(inv, low_stock_threshold=5)
    text = format_summary_text(summary)
    assert "Ringkasan Inventori" in text
    assert "BRG-00101" in text


def test_format_summary_text_without_low_stock():
    inv = Inventory()
    inv.add_item("BRG-00101", "Kabel HDMI", 50, 45000)
    summary = generate_summary(inv, low_stock_threshold=5)
    text = format_summary_text(summary)
    assert "Barang stok menipis: 0" in text
    assert "SKU stok menipis" not in text


def test_run_demo_executes_without_error(capsys):
    run_demo()
    captured = capsys.readouterr()
    assert "Ringkasan Inventori" in captured.out
