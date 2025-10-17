from src.domain.inventory import adjust_stock, create_inventory_item


def test_create_inventory_item():
    ok, item = create_inventory_item({"kode":"B10","nama":"Gula","satuan":"kg","stok":5,"reorder_point":1})
    assert ok
    assert item["stok"] == 5.0


def test_adjust_stock():
    inv = [{"kode":"B1","nama":"X","satuan":"kg","stok":10,"reorder_point":2}]
    new = adjust_stock(inv, "B1", -2)
    assert new[0]["stok"] == 8.0
