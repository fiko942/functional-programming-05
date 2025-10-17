#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

try:
    # Try to import rich + prompt_toolkit for a nicer interactive UI.
    from prompt_toolkit import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout, HSplit
    from prompt_toolkit.widgets import Box, Frame
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.styles import Style
    from prompt_toolkit.shortcuts import yes_no_dialog
    from rich.console import Console
    from rich.panel import Panel

    HAVE_UI = True
except Exception:
    HAVE_UI = False

if HAVE_UI:
    console = Console()

    MENU = [
        ("Seed data", "seed"),
        ("Menu management", "menu_mgmt"),
        ("Inventory management", "inv_mgmt"),
        ("Sales (create order)", "sales_mgmt"),
        ("Purchases (PO)", "po_mgmt"),
        ("Reports", "reports"),
        ("Quit", "quit")
    ]

    style = Style.from_dict({
        "menu-item": "bg:#003366 #ffffff",
        "menu-selected": "bg:#ffffff #000000 bold",
    })

    class Menu:
        def __init__(self, items):
            self.items = items
            self.index = 0
            self.control = FormattedTextControl(self.get_text)
            self.window = Window(content=self.control, height=len(items)+2, style="class:menu-item")

        def get_text(self):
            result = []
            for i,(label,key) in enumerate(self.items):
                prefix = "➤ " if i==self.index else "  "
                style = "class:menu-selected" if i==self.index else ""
                result.append((style, prefix + label + "\n"))
            return result

        def up(self):
            if self.index>0:
                self.index -= 1

        def down(self):
            if self.index < len(self.items)-1:
                self.index += 1

        def selected(self):
            return self.items[self.index][1]


    kb = KeyBindings()

    @kb.add("up")
    def _(event):
        menu.up()

    @kb.add("down")
    def _(event):
        menu.down()

    @kb.add("enter")
    def _(event):
        sel = menu.selected()
        if sel=="quit":
            event.app.exit()
            return
        event.app.exit(result=sel)

    menu = Menu(MENU)

    root_container = HSplit([
        Frame(Window(height=1, content=FormattedTextControl([("","\n  ") , ("class:menu-item","Welcome to Golden Dragon Wok CLI\n")] )), style="bg:#202020 #ffffff"),
        Box(body=menu.window, padding=1),
    ])

    app = Application(layout=Layout(root_container), key_bindings=kb, style=style, full_screen=True)


    # repository / domain imports used by interactive menus
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

    def show_table(items: list[dict], title: str = ""):
        from rich.table import Table
        if not items:
            console.print(Panel("(empty)", title=title))
            return
        keys = list({k for it in items for k in it.keys()})
        table = Table(title=title)
        for k in keys:
            table.add_column(k)
        for it in items:
            row = [str(it.get(k, "")) for k in keys]
            table.add_row(*row)
        console.print(table)

    def action_seed():
        console.print(Panel("Seeding data..."))
        Path("data").mkdir(exist_ok=True)
        seed_data(REPO_PATH)
        console.print(Panel("Seed complete", style="green"))

    def menu_management():
        while True:
            console.print(Panel("Menu Management", style="cyan"))
            console.print("1) List menu\n2) Add menu\n3) Back")
            choice = prompt("Choose")
            if choice == "1":
                items = repo.load_all("menu")
                show_table(items, "Menu")
            elif choice == "2":
                kode = prompt("Kode")
                nama = prompt("Nama")
                kategori = prompt("Kategori", "Main")
                try:
                    harga = float(prompt("Harga", "0"))
                except Exception:
                    console.print("Invalid harga", style="red")
                    continue
                ok, normalized = menu_mod.create_menu_item({"kode":kode,"nama":nama,"kategori":kategori,"harga":harga,"status_tersedia":True})
                if not ok:
                    console.print(f"Error: {normalized}", style="red")
                else:
                    repo.insert("menu", normalized)
                    console.print("Menu added", style="green")
            else:
                break

    def inventory_management():
        while True:
            console.print(Panel("Inventory Management", style="cyan"))
            console.print("1) List inventory\n2) Adjust stock\n3) Add item\n4) Back")
            choice = prompt("Choose")
            if choice == "1":
                items = repo.load_all("inventory")
                show_table(items, "Inventory")
            elif choice == "2":
                kode = prompt("Kode")
                try:
                    delta = float(prompt("Delta (e.g. -2 or 5)", "0"))
                except Exception:
                    console.print("Invalid number", style="red")
                    continue
                items = repo.load_all("inventory")
                new = inv_mod.adjust_stock(items, kode, delta)
                repo.save_all("inventory", new)
                console.print("Stock adjusted", style="green")
            elif choice == "3":
                kode = prompt("Kode")
                nama = prompt("Nama")
                satuan = prompt("Satuan", "unit")
                try:
                    stok = float(prompt("Stok", "0"))
                    rop = float(prompt("Reorder point", "0"))
                except Exception:
                    console.print("Invalid number", style="red")
                    continue
                ok,item = inv_mod.create_inventory_item({"kode":kode,"nama":nama,"satuan":satuan,"stok":stok,"reorder_point":rop})
                if not ok:
                    console.print(f"Error: {item}", style="red")
                else:
                    repo.insert("inventory", item)
                    console.print("Inventory item added", style="green")
            else:
                break

    def sales_management():
        console.print(Panel("Create Sale", style="magenta"))
        order_id = prompt("Order ID")
        order = sales_mod.create_order(order_id, None, "dine-in")
        while True:
            console.print("Add item to order - enter menu kode (or blank to finish)")
            kode = prompt("Menu kode (blank to finish)")
            if not kode:
                break
            menu_item = repo.get("menu", "kode", kode)
            if not menu_item:
                console.print("Menu tidak ditemukan", style="red")
                continue
            try:
                qty = float(prompt("Qty", "1"))
            except Exception:
                console.print("Invalid qty", style="red")
                continue
            order = sales_mod.add_item_to_order(order, menu_item, qty, 0.0)
            console.print(f"Added {menu_item['nama']} x{qty}")
        # close order - check stock
        recipes = repo.load_all("recipes")
        inventory = repo.load_all("inventory")
        ok, result = sales_mod.close_order(order, recipes, inventory)
        if not ok:
            console.print(f"Cannot close order: {result}", style="red")
            return
        closed_order = result["order"]
        new_inventory = result["inventory"]
        repo.insert("sales", closed_order)
        repo.save_all("inventory", new_inventory)
        console.print("Order closed", style="green")
        show_table([closed_order.get("pricing",{})], "Pricing")

    def po_management():
        console.print(Panel("Create Purchase Order", style="magenta"))
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
                console.print("Invalid qty", style="red")
                continue
            lines.append({"kode":kode, "qty":qty})
        po = purchase_mod.create_po(po_id, supplier, lines)
        new_po, new_inv = purchase_mod.receive_po(po, repo.load_all("inventory"))
        repo.insert("purchases", new_po)
        repo.save_all("inventory", new_inv)
        console.print("PO received and inventory updated", style="green")

    def reports_menu():
        while True:
            console.print(Panel("Reports", style="cyan"))
            console.print("1) Sales by date\n2) Low stock\n3) Top selling menu\n4) Back")
            choice = prompt("Choose")
            if choice == "1":
                date = prompt("Date (YYYY-MM-DD)", "2025-10-17")
                sales = repo.load_all("sales")
                gen = reports_mod.sales_by_date_generator(sales, date)
                daily = reports_mod.daily_sales_total(gen)
                console.print(Panel(f"Sales for {date}"))
                try:
                    while True:
                        rec = next(daily)
                        console.print(rec)
                except StopIteration:
                    console.print("End")
            elif choice == "2":
                inv = repo.load_all("inventory")
                gen = inv_mod.low_stock_alerts(inv)
                console.print(Panel("Low stock items"))
                for it in gen:
                    console.print(it)
            elif choice == "3":
                sales = repo.load_all("sales")
                top = reports_mod.top_selling_menu(sales, 5)
                show_table(top, "Top selling")
            else:
                break

    def run_action(action: str):
        if action == "seed":
            action_seed()
        elif action == "menu_mgmt":
            menu_management()
        elif action == "inv_mgmt":
            inventory_management()
        elif action == "sales_mgmt":
            sales_management()
        elif action == "po_mgmt":
            po_management()
        elif action == "reports":
            reports_menu()


    if __name__ == "__main__":
        while True:
            result = app.run()
            if result is None:
                break
            run_action(result)
            if not yes_no_dialog(title="Continue?", text="Return to menu?").run():
                break
        console.print(Panel("Goodbye from Golden Dragon Wok", style="bold green"))

else:
    # Fallback when rich/prompt_toolkit are not installed: show helpful message
    def fallback():
        sep = "="*40
        print(sep)
        print("Golden Dragon Wok interactive UI requires additional packages:")
        print("  pip install -r requirements.txt")
        print("")
        print("You can run the legacy CLI instead:")
        print("  python3 -m src.cli.main")
        print(sep)
        # Ask user whether to run legacy CLI
        try:
            ans = input("Run legacy CLI now? [y/N]: ") or "n"
        except Exception:
            ans = "n"
        if ans.strip().lower().startswith("y"):
            subprocess.run([sys.executable, "-m", "src.cli.main"]) 

    if __name__ == "__main__":
        fallback()
