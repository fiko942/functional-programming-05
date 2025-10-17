from __future__ import annotations
from typing import Iterable
from .validation import non_negative_number, required_fields

# pure inventory logic

def create_inventory_item(item: dict) -> tuple[bool, dict]:
    ok,msg = required_fields(item, ["kode","nama","satuan","stok","reorder_point"])
    if not ok:
        return False,{"error":msg}
    ok,msg = non_negative_number(item.get("stok"), "stok")
    if not ok:
        return False,{"error":msg}
    ok,msg = non_negative_number(item.get("reorder_point"), "reorder_point")
    if not ok:
        return False,{"error":msg}
    normalized = {"kode":item["kode"],"nama":item["nama"],"satuan":item["satuan"],"stok":float(item["stok"]),"reorder_point":float(item["reorder_point"])}
    return True, normalized


def adjust_stock(inventory: Iterable[dict], kode: str, delta: float) -> list[dict]:
    # returns new inventory list after applying delta to kode
    def apply(it):
        if it["kode"] != kode:
            return dict(it)
        new = dict(it)
        new["stok"] = float(new.get("stok",0)) + float(delta)
        return new
    return [apply(it) for it in inventory]


def low_stock_alerts(inventory: Iterable[dict]):
    return (it for it in inventory if float(it.get("stok",0)) < float(it.get("reorder_point",0)))
