from __future__ import annotations
from typing import Iterable, Dict

DEFAULT_TAX = 0.10
DEFAULT_SERVICE = 0.05

# pure price calculation

def line_total(price: float, qty: float, discount: float=0.0) -> float:
    # discount as absolute or percent? we'll treat discount as absolute amount per line
    return max(0.0, float(price)*float(qty) - float(discount))

def subtotal(lines: Iterable[dict]) -> float:
    return float(sum(line_total(l["price"], l.get("qty",1), l.get("discount",0)) for l in lines))

def taxes(subtotal_amount: float, tax_rate: float=DEFAULT_TAX) -> float:
    return float(subtotal_amount) * float(tax_rate)

def service_charge(subtotal_amount: float, service_rate: float=DEFAULT_SERVICE) -> float:
    return float(subtotal_amount) * float(service_rate)


def total_amount(lines: Iterable[dict], tax_rate: float=DEFAULT_TAX, service_rate: float=DEFAULT_SERVICE) -> dict:
    sub = subtotal(lines)
    tax = taxes(sub, tax_rate)
    service = service_charge(sub, service_rate)
    total = sub + tax + service
    return {"subtotal":sub, "tax":tax, "service":service, "total":total}
