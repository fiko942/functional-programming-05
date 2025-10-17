from __future__ import annotations
from typing import Iterable, Dict
from itertools import islice

# pure reports - use generators for lazy streaming

def sales_by_date_generator(sales: Iterable[dict], date: str) -> Iterable[dict]:
    # assume each sale has date field like '2025-10-17'
    for s in sales:
        if s.get("date")==date:
            yield s

def daily_sales_total(sales_gen: Iterable[dict]):
    # consume generator lazily and compute totals per order
    for s in sales_gen:
        items = s.get("items",[])
        total = sum(it.get("price",0)*it.get("qty",1) - it.get("discount",0) for it in items)
        yield {"order_id":s.get("order_id"), "total":total}


def low_stock_report(generator_of_inventory: Iterable[dict]):
    # directly return generator (lazy)
    return (it for it in generator_of_inventory if float(it.get("stok",0)) < float(it.get("reorder_point",0)))


def top_selling_menu(sales: Iterable[dict], top_n: int=5) -> list[dict]:
    counts = {}
    for s in sales:
        for it in s.get("items",[]):
            counts[it["menu_kode"]] = counts.get(it["menu_kode"],0) + it.get("qty",1)
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [{"menu_kode":k, "qty":v} for k,v in ranked[:top_n]]
