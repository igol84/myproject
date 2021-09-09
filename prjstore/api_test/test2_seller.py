import unittest
from prjstore.db import API_DB

count_rows = 0
db = API_DB()

def setUpModule():
    sellers = db.get_all_sellers()
    global count_rows
    count_rows = len(sellers)


def tearDownModule():
    sellers = db.get_all_sellers()
    global count_rows
    assert count_rows == len(sellers), f" count seller changed '"


class TestSeller(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        new_seller = db.create_seller(store_id=1, name="Igor")
        cls.obj_id = list(new_seller)[0]

    def test_case01_get(self):
        seller = db.get_seller(self.obj_id)
        self.assertEqual(seller.name, 'Igor')

    def test_case02_update(self):
        seller = db.update_seller(seller_id=self.obj_id, store_id=1, name="Anna")
        self.assertEqual(list(seller.values())[0].name, 'Anna')

    @classmethod
    def tearDownClass(cls):
        db.delete_seller(seller_id=cls.obj_id)
