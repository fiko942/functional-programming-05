from __future__ import annotations
from typing import Iterable, Dict

# recipes: pure functions mapping menu->bahan

def get_ingredients_for_menu(recipes: Iterable[dict], menu_kode: str) -> list[dict]:
    return next((r["bahan"] for r in recipes if r.get("menu_kode") == menu_kode), [])

def can_make_with_stock(recipe: list[dict], inventory: Iterable[dict], qty: float=1.0) -> bool:
    inv_map = {it["kode"]: float(it["stok"]) for it in inventory}
    return all(inv_map.get(ing["kode"],0) >= ing.get("qty",0)*qty for ing in recipe)

def deduct_inventory(inventory: Iterable[dict], recipe: list[dict], qty: float=1.0) -> list[dict]:
    inv_map = {it["kode"]: dict(it) for it in inventory}
    for ing in recipe:
        k = ing["kode"]
        amount = ing.get("qty",0)*qty
        inv_map[k]["stok"] = float(inv_map[k].get("stok",0)) - amount
    return list(inv_map.values())
