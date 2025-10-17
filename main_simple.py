#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from src.data.json_repo import JSONRepository
from src.data.seed import seed as seed_data
from src.domain import menu as menu_mod
from src.domain import inventory as inv_mod
from src.domain import reports as reports_mod
from src.domain import sales as sales_mod
from src.domain import purchase as purchase_mod

REPO_PATH = Path.cwd() / "data"
repo = JSONRepository(REPO_PATH)


def prompt(text: str, default: str | None = None) -> str:
    if default is not None:
        return input(f"{text} [{default}]: ") or default
    return input(f"{text}: ")


def print_table(items: list[dict]):
    if not items:
        print("(empty)")
        return
    keys = list({k for it in items for k in it.keys()})
    # compute widths
    widths = {k: max(len(str(k)), max((len(str(it.get(k,''))) for it in items), default=0)) for k in keys}
    # header
    header = " | ".join(k.ljust(widths[k]) for k in keys)
    sep = "-+-".join("-"*widths[k] for k in keys)
    print(header)
    print(sep)
    for it in items:
        row = " | ".join(str(it.get(k,'')).ljust(widths[k]) for k in keys)
        print(row)
    print()


def do_seed():
    Path("data").mkdir(exist_ok=True)
    seed_data(REPO_PATH)
    print("Seed complete")


def menu_management():
    while True:
        print("\nMENU MANAGEMENT")
        print("1) List menu")
        print("2) Add menu")
        print("3) Back")
        c = prompt("Choose")
        if c == "1":
            items = repo.load_all("menu")
            print_table(items)
        elif c == "2":
            kode = prompt("Kode")
            nama = prompt("Nama")
            kategori = prompt("Kategori (default Main)", "Main")
            try:
                harga = float(prompt("Harga", "0"))
            except Exception:
                print("Invalid harga")
                continue
            ok, normalized = menu_mod.create_menu_item({"kode":kode,"nama":nama,"kategori":kategori,"harga":harga,"status_tersedia":True})
            if not ok:
                print("Error:", normalized)
            else:
                repo.insert("menu", normalized)
                print("Menu added")
        else:
            break


def inventory_management():
    while True:
        print("\nINVENTORY MANAGEMENT")
        print("1) List inventory")
        print("2) Adjust stock")
        print("3) Add item")
        print("4) Back")
        c = prompt("Choose")
        if c == "1":
            items = repo.load_all("inventory")
            print_table(items)
        elif c == "2":
            kode = prompt("Kode")
            try:
                delta = float(prompt("Delta (e.g. -2 or 5)", "0"))
            except Exception:
                print("Invalid number")
                continue
            items = repo.load_all("inventory")
            new = inv_mod.adjust_stock(items, kode, delta)
            repo.save_all("inventory", new)
            print("Stock adjusted")
        elif c == "3":
            kode = prompt("Kode")
            nama = prompt("Nama")
            satuan = prompt("Satuan", "unit")
            try:
                stok = float(prompt("Stok", "0"))
                rop = float(prompt("Reorder point", "0"))
            except Exception:
                print("Invalid number")
                continue
            ok,item = inv_mod.create_inventory_item({"kode":kode,"nama":nama,"satuan":satuan,"stok":stok,"reorder_point":rop})
            if not ok:
                print("Error:", item)
            else:
                repo.insert("inventory", item)
                print("Inventory item added")
        else:
            break


def sales_management():
    print("\nCREATE SALE")
    order_id = prompt("Order ID")
    order = sales_mod.create_order(order_id, None, "dine-in")
    while True:
        kode = prompt("Menu kode (blank to finish)")
        if not kode:
            break
        menu_item = repo.get("menu","kode",kode)
        if not menu_item:
            print("Menu not found")
            continue
        try:
            qty = float(prompt("Qty", "1"))
        except Exception:
            print("Invalid qty")
            continue
        order = sales_mod.add_item_to_order(order, menu_item, qty, 0.0)
        print(f"Added {menu_item['nama']} x{qty}")
    recipes = repo.load_all("recipes")
    inventory = repo.load_all("inventory")
    ok, result = sales_mod.close_order(order, recipes, inventory)
    if not ok:
        print("Cannot close order:", result)
        return
    closed_order = result["order"]
    new_inventory = result["inventory"]
    repo.insert("sales", closed_order)
    repo.save_all("inventory", new_inventory)
    print("Order closed. Pricing:")
    print_table([closed_order.get("pricing",{})])


def po_management():
    print("\nCREATE PURCHASE ORDER")
    po_id = prompt("PO ID")
    supplier = prompt("Supplier kode")
    lines = []
    while True:
        kode = prompt("Bahan kode (blank finish)")
        if not kode:
            break
        try:
            qty = float(prompt("Qty", "0"))
        except Exception:
            print("Invalid qty")
            continue
        lines.append({"kode":kode, "qty":qty})
    po = purchase_mod.create_po(po_id, supplier, lines)
    new_po, new_inv = purchase_mod.receive_po(po, repo.load_all("inventory"))
    repo.insert("purchases", new_po)
    repo.save_all("inventory", new_inv)
    print("PO received and inventory updated")


def reports_menu():
    while True:
        print("\nREPORTS")
        print("1) Sales by date")
        print("2) Low stock")
        print("3) Top selling menu")
        print("4) Back")
        c = prompt("Choose")
        if c == "1":
            date = prompt("Date (YYYY-MM-DD)", "2025-10-17")
            sales = repo.load_all("sales")
            gen = reports_mod.sales_by_date_generator(sales, date)
            daily = reports_mod.daily_sales_total(gen)
            try:
                while True:
                    rec = next(daily)
                    print(rec)
            except StopIteration:
                print("End")
        elif c == "2":
            inv = repo.load_all("inventory")
            gen = inv_mod.low_stock_alerts(inv)
            for it in gen:
                print(it)
        elif c == "3":
            sales = repo.load_all("sales")
            top = reports_mod.top_selling_menu(sales, 5)
            print_table(top)
        else:
            break


def main():
    while True:
        print("\nGOLDEN DRAGON WOK - MENU")
        print("1) Seed data")
        print("2) Menu management")
        print("3) Inventory management")
        print("4) Sales (create order)")
        print("5) Purchases (PO)")
        print("6) Reports")
        print("7) Quit")
        choice = prompt("Choose")
        if choice == "1":
            do_seed()
        elif choice == "2":
            menu_management()
        elif choice == "3":
            inventory_management()
        elif choice == "4":
            sales_management()
        elif choice == "5":
            po_management()
        elif choice == "6":
            reports_menu()
        else:
            print("Goodbye")
            break

if __name__ == "__main__":
    main()
