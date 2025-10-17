#!/usr/bin/env python3
from __future__ import annotations
from typing import Iterable, Dict, Tuple, Generator
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from functools import reduce

from src.data.json_repo import JSONRepository
from src.domain import pricing as pricing_mod
from src.domain import reports as reports_mod

REPO_PATH = "data"

# --- Pure, declarative reporting functions (no I/O) ---

def parse_date(date_str: str) -> datetime | None:
    if not date_str:
        return None
    # try ISO first
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        pass
    # common formats
    fmts = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]
    for f in fmts:
        try:
            return datetime.strptime(date_str, f)
        except Exception:
            continue
    # try epoch seconds
    try:
        if str(date_str).isdigit():
            ts = int(date_str)
            # if milliseconds, convert
            if ts > 1_000_000_000_000:
                ts = ts / 1000
            return datetime.fromtimestamp(ts)
    except Exception:
        pass
    return None


def extract_date_str_from_sale(sale: dict) -> str | None:
    """Pure helper: look for a sensible date string in a sale record.

    Checks common keys ('date','created_at','timestamp','datetime') and returns
    the first non-empty value as a string, or None.
    """
    for key in ("date", "created_at", "datetime", "timestamp", "time"):
        v = sale.get(key)
        if v:
            return str(v)
    return None


def sale_revenue(sale: dict) -> float:
    """Pure: compute total revenue for a sale using pricing.total_amount.

    Returns the 'total' field (subtotal + tax + service).
    """
    lines = sale.get("items", [])
    # each line expected to have price, qty, discount
    t = pricing_mod.total_amount(lines)
    return float(t.get("total", 0.0))


def sales_by_period_key(date: str, period: str) -> str:
    dt = parse_date(date)
    if dt is None:
        return "(no date)"
    if period == "day":
        return dt.strftime("%Y-%m-%d")
    if period == "week":
        y, w, _ = dt.isocalendar()
        return f"{y}-W{w:02d}"
    if period == "month":
        return dt.strftime("%Y-%m")
    if period == "year":
        return dt.strftime("%Y")
    raise ValueError("unknown period")


def aggregate_revenue_by_period(sales: Iterable[dict], period: str = "day") -> Dict[str, float]:
    """Pure: aggregate revenue per period key (day/week/month/year)."""
    # build list of (key, revenue)
    pairs = [ (sales_by_period_key(extract_date_str_from_sale(s) or "", period), sale_revenue(s)) for s in sales ]
    # group by key
    grouped: Dict[str, float] = {}
    for k, rev in pairs:
        grouped[k] = grouped.get(k, 0.0) + float(rev)
    return grouped


def revenue_by_period_generator(sales: Iterable[dict], period: str = "day") -> Generator[Tuple[str, float], None, None]:
    """Lazy generator yielding (period_key, revenue) sorted by period_key ascending."""
    agg = aggregate_revenue_by_period(sales, period)
    for k in sorted(agg.keys()):
        yield (k, agg[k])


def top_selling(sales: Iterable[dict], top_n: int = 3) -> list[dict]:
    """Pure: compute top selling menu items using domain.reports.top_selling_menu and
    enrich with revenue per menu item."""
    # use domain function to get top menu_kode and qty
    top = reports_mod.top_selling_menu(sales, top_n)
    # compute revenue per menu_kode
    revenue_map: Dict[str, float] = {}
    for s in sales:
        for it in s.get("items", []):
            kode = it.get("menu_kode")
            rev = float(it.get("price",0)) * float(it.get("qty",1)) - float(it.get("discount",0))
            revenue_map[kode] = revenue_map.get(kode, 0.0) + rev
    # combine
    enriched = [ {**r, "revenue": float(revenue_map.get(r["menu_kode"], 0.0))} for r in top ]
    return enriched


# --- I/O: print reports by consuming pure functions ---

def _print_section(title: str):
    print("\n" + "="*40)
    print(title)
    print("="*40 + "\n")


def main():
    repo = JSONRepository(REPO_PATH)
    sales = repo.load_all("sales")

    # Normalize sale date fields: if a sale lacks a parseable date, try to infer
    # from known keys; otherwise default to today. Persist normalization back
    # so subsequent reports have dates.
    def normalize_sales_dates(sales_list: list[dict]) -> list[dict]:
        changed = False
        normalized = []
        today = datetime.now().strftime("%Y-%m-%d")
        updated_ids = []
        for s in sales_list:
            date_str = extract_date_str_from_sale(s)
            dt = parse_date(date_str or "")
            if dt is None:
                # set to today
                s2 = dict(s)
                s2["date"] = today
                normalized.append(s2)
                changed = True
                updated_ids.append(s2.get("order_id") or s2.get("id") or "(no-id)")
            else:
                s2 = dict(s)
                s2["date"] = dt.strftime("%Y-%m-%d")
                normalized.append(s2)
        if changed:
            repo.save_all("sales", normalized)
            print(f"Normalized {len(updated_ids)} sale(s) dates and saved to repository: {updated_ids}")
        return normalized

    sales = normalize_sales_dates(sales)

    _print_section("Top selling menus (top 3)")
    top3 = top_selling(sales, 3)
    if not top3:
        print("(no sales data)")
    else:
        # compute column widths
        kode_w = max((len(str(r.get("menu_kode"))) for r in top3), default=4)
        qty_w = max((len(str(r.get("qty"))) for r in top3), default=3)
        rev_w = max((len(f"{r.get('revenue'):.2f}") for r in top3), default=7)
        print(f"{'#':>2}  {'Menu':{kode_w}}  {'Qty':>{qty_w}}  {'Revenue':>{rev_w}}")
        print('-'*(6 + kode_w + qty_w + rev_w))
        for i, r in enumerate(top3, start=1):
            print(f"{i:>2}. {str(r.get('menu_kode')):{kode_w}}  {r.get('qty'):>{qty_w}}  {r.get('revenue'):{rev_w}.2f}")
        total_rev = sum(r.get('revenue',0.0) for r in top3)
        print('-'*(6 + kode_w + qty_w + rev_w))
        print(f"{'':>2}  {'Total':{kode_w}}  {'':>{qty_w}}  {total_rev:{rev_w}.2f}")

    # revenue per day/week/month/year
    for period in ("day","week","month","year"):
        _print_section(f"Revenue per {period}")
        gen = revenue_by_period_generator(sales, period)
        # collect to list for aligned print
        rows = list(gen)
        if not rows:
            print("(no data)")
            continue
        key_w = max(len(k) for k,_ in rows)
        rev_w = max(len(f"{v:.2f}") for _,v in rows)
        for k,v in rows:
            print(f"{k:{key_w}} : {v:{rev_w}.2f}")
        grand = sum(v for _,v in rows)
        print('-'*(key_w + 3 + rev_w))
        print(f"{'Grand Total':{key_w}} : {grand:{rev_w}.2f}")


if __name__ == "__main__":
    main()
