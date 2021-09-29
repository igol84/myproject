import unittest
from prjstore.db import API_DB

count_rows = 0
db = API_DB()


def setUpModule():
    sale_line_items = db.sale_line_item.get_all()
    global count_rows
    count_rows = len(sale_line_items)


def tearDownModule():
    sale_line_items = db.sale_line_item.get_all()
    global count_rows
    assert count_rows == len(sale_line_items), f" count sale_line_item changed '"


class TestSaleLineItem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.sale_line_item.create(sale_id=1, item_id=2, sale_price=1100, qty=1)

    def test_case01_get(self):
        sale_line_item = db.sale_line_item.get(sale_id=1, item_id=2, sale_price=1100)
        self.assertEqual(sale_line_item.sale_price.amount, 1100)
        self.assertEqual(sale_line_item.qty, 1)

    def test_case02_update(self):
        sale_line_item = db.sale_line_item.update(sale_id=1, item_id=2, sale_price=1100, qty=2)
        self.assertEqual(sale_line_item.qty, 2)

    @classmethod
    def tearDownClass(cls):
        db.sale_line_item.delete(sale_id=1, item_id=2, sale_price=1100)
