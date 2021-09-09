import unittest
import requests
from prjstore.schemas.seller import CreateSeller, Seller
from prjstore.api_test.authorization import host, headers

prefix = '/seller'
count_rows = 0


def setUpModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    count_rows = len(r.json())


def tearDownModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    assert count_rows == len(r.json()), f" count seller changed '"


class TestSeller(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        new_seller = CreateSeller(store_id=1, name="Igor")
        r = requests.post(
            f'{host}{prefix}/',
            json=new_seller.dict(),
            headers=headers
        )
        seller = Seller(**r.json())
        cls.obj_id = seller.id

    def test_case01_get(self):
        r = requests.get(f"{host}{prefix}/{self.obj_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        seller = Seller(**r.json())
        self.assertEqual(seller.store_id, 1)
        self.assertEqual(seller.name, 'Igor')

    def test_case02_update(self):
        new_seller = CreateSeller(store_id=2, name="Anna")
        r = requests.put(
            f"{host}{prefix}/{self.obj_id}",
            json=new_seller.dict(),
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}{prefix}/{self.obj_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        seller = Seller(**r.json())
        self.assertEqual(seller.store_id, 2)
        self.assertEqual(seller.name, 'Anna')

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}{prefix}/{cls.obj_id}", headers=headers)
