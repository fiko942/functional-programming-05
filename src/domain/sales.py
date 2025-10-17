from __future__ import annotations
from typing import Iterable
from .pricing import line_total, total_amount
from .recipes import get_ingredients_for_menu, can_make_with_stock, deduct_inventory

# sales domain pure functions

def create_order(order_id: str, customer: dict | None, order_type: str="dine-in") -> dict:
    return {"order_id":order_id, "customer":customer or {}, "type":order_type, "items":[], "status":"open"}

def add_item_to_order(order: dict, menu_item: dict, qty: float=1.0, discount: float=0.0) -> dict:
    item = {"menu_kode":menu_item["kode"], "name":menu_item["nama"], "price":float(menu_item["harga"]), "qty":float(qty), "discount":float(discount)}
    new = dict(order)
    new_items = [*order.get("items",[]), item]
    new["items"] = new_items
    return new


def void_item(order: dict, index: int) -> dict:
    new = dict(order)
    items = list(order.get("items",[]))
    if 0 <= index < len(items):
        items.pop(index)
    new["items"] = items
    return new


def close_order(order: dict, recipes: Iterable[dict], inventory: Iterable[dict], tax_rate: float=0.1, service_rate: float=0.05) -> tuple[bool, dict]:
    # check stock availability
    items = order.get("items",[])
    # aggregate needed ingredients
    needed = {}
    for it in items:
        recipe = get_ingredients_for_menu(recipes, it["menu_kode"]) or []
        for ing in recipe:
            needed[ing["kode"]] = needed.get(ing["kode"],0) + ing.get("qty",0) * it.get("qty",1)
    # verify stock
    inv_map = {i["kode"]: float(i.get("stok",0)) for i in inventory}
    for kode, req in needed.items():
        if inv_map.get(kode,0) < req:
            return False, {"error":f"Bahan {kode} tidak cukup"}
    # deduct inventory
    new_inventory = list(inventory)
    for kode, req in needed.items():
        new_inventory = [ {**it, "stok": (float(it.get("stok",0)) - req) } if it["kode"]==kode else it for it in new_inventory]
    # compute pricing
    pricing = total_amount(items, tax_rate, service_rate)
    closed = {**order, "status":"closed", "pricing":pricing}
    return True, {"order":closed, "inventory":new_inventory}
