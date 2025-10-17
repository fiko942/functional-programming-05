from __future__ import annotations

def non_negative_number(value: float, name: str) -> tuple[bool,str]:
    if value is None:
        return False, f"{name} tidak boleh kosong"
    try:
        v = float(value)
    except Exception:
        return False, f"{name} harus berupa angka"
    if v < 0:
        return False, f"{name} tidak boleh negatif"
    return True, ""

def required_fields(data: dict, fields: list[str]) -> tuple[bool,str]:
    missing = [f for f in fields if f not in data or data[f] in (None,"")]
    if missing:
        return False, f"Field yang hilang: {', '.join(missing)}"
    return True, ""
