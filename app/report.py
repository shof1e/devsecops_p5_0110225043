"""Modul untuk menghasilkan ringkasan laporan inventori."""

from app.inventory import Inventory


def generate_summary(inventory: Inventory, low_stock_threshold: int = 5) -> dict:
    """Menghasilkan ringkasan singkat kondisi inventori saat ini."""
    low_stock = inventory.low_stock_items(threshold=low_stock_threshold)
    return {
        "total_sku": len(inventory._items),
        "total_value": round(inventory.total_value(), 2),
        "low_stock_count": len(low_stock),
        "low_stock_skus": [item.sku for item in low_stock],
    }


def format_summary_text(summary: dict) -> str:
    """Mengubah ringkasan (dict) menjadi teks yang mudah dibaca."""
    lines = [
        "=== Ringkasan Inventori ===",
        f"Total jenis barang (SKU): {summary['total_sku']}",
        f"Total nilai inventori: Rp{summary['total_value']:,.2f}",
        f"Barang stok menipis: {summary['low_stock_count']}",
    ]
    if summary["low_stock_skus"]:
        lines.append("SKU stok menipis: " + ", ".join(summary["low_stock_skus"]))
    return "\n".join(lines)
