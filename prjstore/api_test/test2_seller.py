import unittest
from prjstore.db import API_DB

count_rows = 0
db = API_DB()


def setUpModule():
    sellers = db.seller.get_all()
    global count_rows
    count_rows = len(sellers)


def tearDownModule():
    sellers = db.seller.get_all()
    global count_rows
    assert count_rows == len(sellers), f" count seller changed '"


class TestSeller(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        new_seller = db.seller.create(store_id=1, name="Igor")
        cls.obj_id = new_seller.id

    def test_case01_get(self):
        seller = db.seller.get(self.obj_id)
        self.assertEqual(seller.name, 'Igor')

    def test_case02_update(self):
        seller = db.seller.update(seller_id=self.obj_id, store_id=1, name="Anna")
        self.assertEqual(seller.name, 'Anna')

    @classmethod
    def tearDownClass(cls):
        db.seller.delete(seller_id=cls.obj_id)
