import unittest
from datetime import datetime

from prjstore.db import API_DB, schemas
from prjstore.db.schemas.sale_line_item import CreateSaleLineItemForSale
from prjstore.domain.sale import Sale

count_rows = 0
db = API_DB()


def setUpModule():
    sales = db.sale.get_all()
    global count_rows
    count_rows = len(sales)


def tearDownModule():
    sales = db.sale.get_all()
    global count_rows
    assert count_rows == len(sales), f" count sale changed '"


class TestSeller(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        sale_line_items = [CreateSaleLineItemForSale(item_id=1, sale_price=1, qty=1),
                           CreateSaleLineItemForSale(item_id=2, sale_price=1, qty=1)]
        pd_sale = schemas.sale.CreateSale(place_id=1, seller_id=1, date_time=datetime.now(),
                                          sale_line_items=sale_line_items)
        new_sale = Sale.create_from_schema(db.sale.create(pd_sale))
        cls.obj_id = new_sale.id

    def test_case01_get(self):
        sale = Sale.create_from_schema(db.sale.get(self.obj_id))
        self.assertEqual(sale.seller.id, 1)
        self.assertEqual(sale.list_sli[0].item.id, 1)
        self.assertEqual(sale.list_sli[1].item.id, 2)

    def test_case02_update(self):
        sale_line_items = [CreateSaleLineItemForSale(item_id=3, sale_price=20, qty=2)]
        pd_sale = schemas.sale.UpdateSale(id=self.obj_id, place_id=2, seller_id=2, date_time=datetime.now(),
                                          sale_line_items=sale_line_items)
        sale = Sale.create_from_schema(db.sale.update(pd_sale))
        self.assertEqual(sale.seller.id, 2)
        self.assertEqual(sale.list_sli[0].item.id, 3)
        self.assertEqual(sale.list_sli[0].sale_price.amount, 20.0)

    @classmethod
    def tearDownClass(cls):
        db.sale.delete(cls.obj_id)
