from __future__ import annotations
from typing import Iterable

# purchases: pure functions

def create_po(po_id: str, supplier_kode: str, lines: Iterable[dict]) -> dict:
    return {"po_id":po_id, "supplier_kode":supplier_kode, "lines":list(lines), "status":"open"}


def receive_po(po: dict, inventory: Iterable[dict]) -> tuple[dict, list[dict]]:
    # return updated po (status closed) and new inventory list
    new_inv = list(inventory)
    for line in po.get("lines",[]):
        kode = line["kode"]
        qty = float(line.get("qty",0))
        new_inv = [ {**it, "stok": float(it.get("stok",0)) + qty } if it["kode"]==kode else it for it in new_inv]
    new_po = {**po, "status":"received"}
    return new_po, new_inv
