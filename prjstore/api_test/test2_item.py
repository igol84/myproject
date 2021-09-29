import unittest
from prjstore.db import API_DB

count_rows = 0
db = API_DB()


def setUpModule():
    items = db.item.get_all()
    global count_rows
    count_rows = len(items)


def tearDownModule():
    items = db.item.get_all()
    global count_rows
    assert count_rows == len(items), f" count item changed '"


class TestSeller(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        new_item = db.item.create(prod_id=2, store_id=1, qty=10, buy_price=10.5)
        cls.obj_id = new_item.id

    def test_case01_get(self):
        item = db.item.get(self.obj_id)
        self.assertEqual(item.product.prod_id, '2')
        self.assertEqual(item.qty, 10)
        self.assertEqual(item.buy_price.amount, 10.5)

    def test_case02_update(self):
        item = db.item.update(item_id=self.obj_id, prod_id=3, store_id=1, qty=12, buy_price=11.5)
        self.assertEqual(item.product.prod_id, '3')
        self.assertEqual(item.qty, 12)
        self.assertEqual(item.buy_price.amount, 11.5)

    @classmethod
    def tearDownClass(cls):
        db.item.delete(item_id=cls.obj_id)
