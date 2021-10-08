import unittest
from prjstore import schemas
from prjstore.db import API_DB
from prjstore.domain.item import Item

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
        pd_item = schemas.item.CreateItem(prod_id=2, store_id=1, qty=10, buy_price=10.5)
        new_item = db.item.create(pd_item)
        cls.obj_id = new_item.id

    def test_case01_get(self):
        item = Item.create_from_schema(db.item.get(self.obj_id))
        self.assertEqual(item.product.prod_id, '2')
        self.assertEqual(item.qty, 10)
        self.assertEqual(item.buy_price.amount, 10.5)

    def test_case02_update(self):
        pd_item = schemas.item.UpdateItem(id=self.obj_id, prod_id=3, store_id=1, qty=12, buy_price=11.5)
        item = Item.create_from_schema(db.item.update(pd_item))
        self.assertEqual(item.product.prod_id, '3')
        self.assertEqual(item.qty, 12)
        self.assertEqual(item.buy_price.amount, 11.5)

    @classmethod
    def tearDownClass(cls):
        db.item.delete(cls.obj_id)
