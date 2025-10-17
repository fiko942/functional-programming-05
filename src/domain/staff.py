from __future__ import annotations
from .validation import required_fields

def create_staff(data: dict) -> tuple[bool, dict]:
    ok,msg = required_fields(data, ["id","nama","role"])
    if not ok:
        return False,{"error":msg}
    return True, {"id":data["id"], "nama":data["nama"], "role":data["role"]}

def list_staff(staffs: list[dict]) -> list[dict]:
    return [dict(s) for s in staffs]
