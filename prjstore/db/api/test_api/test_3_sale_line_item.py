from prjstore.db import API_DB
from prjstore.db.schemas import sale_line_item as schemas
from prjstore.domain.sale_line_item import SaleLineItem

count_rows = 0
db = API_DB()


def setup_method():
    sale_line_items = db.sale_line_item.get_all()
    global count_rows
    count_rows = len(sale_line_items)


def teardown_method():
    sale_line_items = db.sale_line_item.get_all()
    global count_rows
    assert count_rows == len(sale_line_items), f" count sale_line_item changed '"


class TestSaleLineItem:

    @classmethod
    def setup_class(cls):
        pd_sli = schemas.CreateSaleLineItem(sale_id=1, item_id=2, sale_price=1100, qty=1)
        db.sale_line_item.create(pd_sli)

    def test_case01_get(self):
        pd_sli = db.sale_line_item.get(sale_id=1, item_id=2, sale_price=1100)
        sale_line_item = SaleLineItem.create_from_schema(pd_sli)
        assert sale_line_item.sale_price.amount == 1100
        assert sale_line_item.qty == 1

    def test_case02_update(self):
        pd_sli = schemas.CreateSaleLineItem(sale_id=1, item_id=2, sale_price=1100, qty=2)
        sale_line_item = SaleLineItem.create_from_schema(db.sale_line_item.update(pd_sli))
        assert sale_line_item.qty == 2

    @classmethod
    def teardown_class(cls):
        db.sale_line_item.delete(sale_id=1, item_id=2, sale_price=1100)
