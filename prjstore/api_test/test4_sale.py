import unittest
from datetime import datetime

from prjstore import schemas
from prjstore.db import API_DB
from prjstore.schemas.sale_line_item import CreateSaleLineItemForSale


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
        new_sale = db.sale.create(new_sale=pd_sale)
        cls.obj_id = new_sale.id

    def test_case01_get(self):
        sale = db.sale.get(self.obj_id)
        self.assertEqual(sale.name, 'Igor')

    def test_case02_update(self):
        sale = db.sale.update(sale_id=self.obj_id, store_id=1, name="Anna")
        self.assertEqual(sale.name, 'Anna')

    @classmethod
    def tearDownClass(cls):
        db.sale.delete(sale_id=cls.obj_id)
