from src.domain.pricing import line_total, total_amount


def test_line_total():
    assert line_total(10000,2,0) == 20000
    assert line_total(10000,2,5000) == 15000
    assert line_total(10000,2,25000) == 0


def test_total_amount():
    lines = [{"price":10000,"qty":2,"discount":0},{"price":5000,"qty":1,"discount":0}]
    res = total_amount(lines, tax_rate=0.1, service_rate=0.05)
    assert res["subtotal"] == 25000
    assert round(res["tax"],2) == 2500.0
    assert round(res["service"],2) == 1250.0
    assert round(res["total"],2) == 28750.0
