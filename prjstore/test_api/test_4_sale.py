from datetime import datetime

from prjstore.db import API_DB, schemas
from prjstore.db.schemas.sale_line_item import CreateSaleLineItemForSale
from prjstore.domain.item import Item
from prjstore.domain.sale import Sale

count_rows = 0
db = API_DB()


def setup_method():
    sales = db.sale.get_all()
    global count_rows
    count_rows = len(sales)


def teardown_method():
    sales = db.sale.get_all()
    global count_rows
    assert count_rows == len(sales), f" count sale changed '"


class TestSeller:
    obj_id: int = None
    items = {1: Item.create_from_schema(db.item.get(1)).qty,
             2: Item.create_from_schema(db.item.get(2)).qty,
             3: Item.create_from_schema(db.item.get(3)).qty}

    @classmethod
    def setup_class(cls):
        sale_line_items = [CreateSaleLineItemForSale(item_id=1, sale_price=1, qty=1),
                           CreateSaleLineItemForSale(item_id=2, sale_price=1, qty=2)]
        pd_sale = schemas.sale.CreateSale(place_id=1, seller_id=1, date_time=datetime.now(),
                                          sale_line_items=sale_line_items)
        new_sale = Sale.create_from_schema(db.sale.create(pd_sale))
        cls.obj_id = new_sale.id

    def test_case01_get(self):
        sale = Sale.create_from_schema(db.sale.get(self.obj_id))
        assert sale.seller.id == 1
        assert sale.list_sli[0].item.id == 1
        assert sale.list_sli[1].item.id == 2
        assert self.items[1] == Item.create_from_schema(db.item.get(1)).qty + 1
        assert self.items[2] == Item.create_from_schema(db.item.get(2)).qty + 2

    def test_case02_update(self):
        sale_line_items = [CreateSaleLineItemForSale(item_id=3, sale_price=20, qty=2)]
        pd_sale = schemas.sale.UpdateSale(id=self.obj_id, place_id=2, seller_id=2, date_time=datetime.now(),
                                          sale_line_items=sale_line_items)
        sale = Sale.create_from_schema(db.sale.update(pd_sale))
        assert sale.seller.id == 2
        assert sale.list_sli[0].item.id == 3
        assert sale.list_sli[0].sale_price.amount, 20.0
        assert self.items[1] == Item.create_from_schema(db.item.get(1)).qty
        assert self.items[2] == Item.create_from_schema(db.item.get(2)).qty
        assert self.items[3] == Item.create_from_schema(db.item.get(3)).qty + 2

    def test_case03_delete(self):
        db.sale.delete(self.obj_id)
        assert self.items[1] == Item.create_from_schema(db.item.get(1)).qty
        assert self.items[2] == Item.create_from_schema(db.item.get(2)).qty
        assert self.items[3] == Item.create_from_schema(db.item.get(3)).qty
