from __future__ import annotations
import argparse
from pathlib import Path
from src.data.json_repo import JSONRepository
from src.data.seed import seed
from src.domain import menu as menu_mod
from src.domain import inventory as inv_mod
from src.domain import reports as reports_mod

REPO_PATH = Path.cwd() / "data"


def cmd_seed(args):
    seed(REPO_PATH)


def cmd_menu(args):
    repo = JSONRepository(REPO_PATH)
    if args.action == "list":
        items = repo.load_all("menu")
        for it in menu_mod.list_menu(items):
            print(it)
    elif args.action == "add":
        item = {"kode":args.kode,"nama":args.nama,"kategori":args.kategori,"harga":args.harga,"status_tersedia":True}
        ok, normalized = menu_mod.create_menu_item(item)
        if not ok:
            print("Error:", normalized)
            return
        repo.insert("menu", normalized)
        print("Added", normalized)


def cmd_inventory(args):
    repo = JSONRepository(REPO_PATH)
    if args.action == "list":
        items = repo.load_all("inventory")
        for it in items:
            print(it)
    elif args.action == "adjust":
        items = repo.load_all("inventory")
        new = inv_mod.adjust_stock(items, args.kode, args.delta)
        repo.save_all("inventory", new)
        print("Adjusted stock for", args.kode)


def cmd_report(args):
    repo = JSONRepository(REPO_PATH)
    if args.type == "sales":
        sales = repo.load_all("sales")
        gen = reports_mod.sales_by_date_generator(sales, args.date)
        daily = reports_mod.daily_sales_total(gen)
        print("Streamed daily sales totals (generator):")
        try:
            while True:
                rec = next(daily)
                print(rec)
        except StopIteration:
            print("End of report")


def main():
    parser = argparse.ArgumentParser(prog="gdw", description="Golden Dragon Wok CLI")
    sub = parser.add_subparsers(dest="cmd")

    seed_p = sub.add_parser("seed")
    seed_p.set_defaults(func=cmd_seed)

    menu_p = sub.add_parser("menu")
    menu_p.add_argument("action", choices=["list","add"])
    menu_p.add_argument("kode", nargs="?")
    menu_p.add_argument("nama", nargs="?")
    menu_p.add_argument("kategori", nargs="?", default="Others")
    menu_p.add_argument("harga", nargs="?", type=float, default=0.0)
    menu_p.set_defaults(func=cmd_menu)

    inv_p = sub.add_parser("inventory")
    inv_p.add_argument("action", choices=["list","adjust"])
    inv_p.add_argument("kode", nargs="?")
    inv_p.add_argument("delta", nargs="?", type=float, default=0.0)
    inv_p.set_defaults(func=cmd_inventory)

    rep_p = sub.add_parser("report")
    rep_p.add_argument("type", choices=["sales","low_stock","top_menu"])
    rep_p.add_argument("date", nargs="?", default="2025-10-17")
    rep_p.set_defaults(func=cmd_report)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
