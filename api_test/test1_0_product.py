import unittest
import requests
from api_test.authorization import host, headers
from prjstore.schemas import product as product_schema

count_rows = 0
prefix = '/prod'


def setUpModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    count_rows = len(r.json())


def tearDownModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    assert count_rows == len(r.json()), f" count prod changed '"


class TestProd(unittest.TestCase):
    prod_id: int = None

    @classmethod
    def setUpClass(cls):
        new_product = product_schema.CreateProduct(type="", name="battery", price=10)
        r = requests.post(
            f'{host}{prefix}/',
            json=new_product.dict(),
            headers=headers
        )
        product = product_schema.Product(**r.json())
        cls.prod_id = product.id

    def test_case01_get(self):
        r = requests.get(f"{host}{prefix}/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        product = product_schema.Product(**r.json())
        self.assertEqual(product, product_schema.Product(id=self.prod_id, type="", name="battery", price=10))

    def test_case02_update(self):
        new_product = product_schema.CreateProduct(type="shoes", name="converse", price=15)
        r = requests.put(
            f"{host}{prefix}/{self.prod_id}",
            json=new_product.dict(),
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}{prefix}/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        product = product_schema.Product(**r.json())
        self.assertEqual(product, product_schema.Product(id=self.prod_id, type="shoes", name="converse", price=15))

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}{prefix}/{cls.prod_id}", headers=headers)
