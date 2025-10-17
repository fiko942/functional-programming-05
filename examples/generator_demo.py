from pathlib import Path
from src.data.json_repo import JSONRepository
from src.data.seed import seed
from src.domain import reports as reports_mod

REPO = Path.cwd() / "data"

if __name__ == "__main__":
    seed(REPO)
    repo = JSONRepository(REPO)
    sales = repo.load_all("sales")
    # prepare a fake sale for demo
    sale = {"order_id":"O001","date":"2025-10-17","items":[{"menu_kode":"M001","price":25000,"qty":1,"discount":0}]}
    repo.insert("sales", sale)
    gen = reports_mod.sales_by_date_generator(repo.load_all("sales"), "2025-10-17")
    daily = reports_mod.daily_sales_total(gen)
    print("Consume generator with next():")
    try:
        while True:
            rec = next(daily)
            print(rec)
    except StopIteration:
        print("Done")
