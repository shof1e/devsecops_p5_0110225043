"""Fungsi-fungsi validasi input untuk modul inventori."""

import re

SKU_PATTERN = re.compile(r"^[A-Z]{2,4}-\d{3,6}$")


def is_valid_sku(sku: str) -> bool:
    """Memeriksa apakah format SKU valid, contoh: 'BRG-00123'."""
    if not isinstance(sku, str):
        return False
    return bool(SKU_PATTERN.match(sku))


def is_valid_quantity(quantity: int) -> bool:
    """Memeriksa apakah jumlah barang adalah bilangan bulat positif."""
    return isinstance(quantity, int) and quantity >= 0


def is_valid_price(price: float) -> bool:
    """Memeriksa apakah harga barang adalah angka non-negatif."""
    return isinstance(price, (int, float)) and price >= 0


def validate_item_input(sku: str, quantity: int, price: float) -> list[str]:
    """Mengumpulkan semua pesan error validasi untuk satu input barang."""
    errors = []
    if not is_valid_sku(sku):
        errors.append(f"SKU '{sku}' tidak sesuai format (contoh: BRG-00123)")
    if not is_valid_quantity(quantity):
        errors.append("Jumlah barang harus bilangan bulat >= 0")
    if not is_valid_price(price):
        errors.append("Harga barang harus angka >= 0")
    return errors
