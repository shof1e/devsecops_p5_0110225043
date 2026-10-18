"""Entry point aplikasi: demo alur kerja manajemen inventori sederhana."""

from app.inventory import Inventory
from app.report import format_summary_text, generate_summary
from app.validators import validate_item_input


def run_demo() -> None:
    """Menjalankan skenario demo: tambah barang, kurangi stok, cetak laporan."""
    inventory = Inventory()

    sample_items = [
        ("BRG-00101", "Kabel HDMI 2m", 20, 45000),
        ("BRG-00102", "Mouse Wireless", 3, 120000),
        ("BRG-00103", "Keyboard Mekanik", 8, 350000),
    ]

    for sku, name, quantity, price in sample_items:
        errors = validate_item_input(sku, quantity, price)
        if errors:
            print(f"Gagal menambah {name}: {errors}")
            continue
        inventory.add_item(sku, name, quantity, price)

    inventory.remove_stock("BRG-00101", 5)

    summary = generate_summary(inventory, low_stock_threshold=5)
    print(format_summary_text(summary))


if __name__ == "__main__":
    run_demo()
