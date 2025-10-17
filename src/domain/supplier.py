from __future__ import annotations
from .validation import required_fields

def create_supplier(data: dict) -> tuple[bool, dict]:
    ok,msg = required_fields(data, ["kode","nama","kontak"])
    if not ok:
        return False,{"error":msg}
    return True, {"kode":data["kode"],"nama":data["nama"],"kontak":data["kontak"]}

def list_suppliers(suppliers: list[dict]) -> list[dict]:
    return [dict(s) for s in suppliers]
