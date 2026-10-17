"""Modul inti untuk mengelola data inventori barang."""

from dataclasses import dataclass, field


@dataclass
class Item:
    """Merepresentasikan satu barang dalam inventori."""

    sku: str
    name: str
    quantity: int
    price: float


class Inventory:
    """Mengelola kumpulan barang (Item) dalam satu gudang."""

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def add_item(self, sku: str, name: str, quantity: int, price: float) -> Item:
        """Menambahkan barang baru. Jika SKU sudah ada, stok akan digabung."""
        if sku in self._items:
            existing = self._items[sku]
            existing.quantity += quantity
            return existing

        item = Item(sku=sku, name=name, quantity=quantity, price=price)
        self._items[sku] = item
        return item

    def remove_stock(self, sku: str, quantity: int) -> Item:
        """Mengurangi stok sebuah barang berdasarkan SKU."""
        if sku not in self._items:
            raise KeyError(f"SKU '{sku}' tidak ditemukan")

        item = self._items[sku]
        if quantity > item.quantity:
            raise ValueError("Stok tidak mencukupi")

        item.quantity -= quantity
        return item

    def get_item(self, sku: str) -> Item | None:
        """Mengambil data satu barang berdasarkan SKU."""
        return self._items.get(sku)

    def total_value(self) -> float:
        """Menghitung total nilai seluruh barang dalam inventori."""
        return sum(item.quantity * item.price for item in self._items.values())

    def low_stock_items(self, threshold: int = 5) -> list[Item]:
        """Mengembalikan daftar barang dengan stok di bawah ambang batas."""
        return [item for item in self._items.values() if item.quantity < threshold]
