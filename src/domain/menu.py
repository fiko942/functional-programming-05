from __future__ import annotations
from typing import Iterable
from .validation import required_fields, non_negative_number

# pure functions for menu CRUD

def create_menu_item(item: dict) -> tuple[bool, dict]:
    ok, msg = required_fields(item, ["kode","nama","kategori","harga","status_tersedia"])
    if not ok:
        return False, {"error":msg}
    ok, msg = non_negative_number(item.get("harga"), "harga")
    if not ok:
        return False, {"error":msg}
    # return normalized item
    normalized = {"kode":item["kode"],"nama":item["nama"],"kategori":item["kategori"],"harga":float(item["harga"]),"status_tersedia":bool(item["status_tersedia"])}
    return True, normalized

def update_menu_item(existing: dict, changes: dict) -> tuple[bool, dict]:
    merged = {**existing, **changes}
    return create_menu_item(merged)

def list_menu(items: Iterable[dict]) -> list[dict]:
    return [ {k:v for k,v in it.items()} for it in items ]
