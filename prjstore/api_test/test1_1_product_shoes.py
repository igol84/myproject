import unittest
import requests
from prjstore.api_test.authorization import host, headers
from prjstore.schemas import product as product_schema
from prjstore.schemas import shoes as shoes_schema

count_rows = 0
prefix = '/shoes'


def setUpModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    count_rows = len(r.json())


def tearDownModule():
    r = requests.get(f"{host}{prefix}", headers=headers)
    global count_rows
    assert count_rows == len(r.json()), f" count prod changed '"


class TestShoes(unittest.TestCase):
    prod_id: int = None

    @classmethod
    def setUpClass(cls):
        new_product = product_schema.CreateProduct(type="shoes", name="converse", price=10)
        r = requests.post(
            f'{host}/prod/',
            json=new_product.dict(),
            headers=headers
        )
        product = product_schema.Product(**r.json())
        print(product)
        cls.prod_id = product.id
        new_shoes = shoes_schema.CreateShoes(id=product.id, color='red', size=41, length=19, width='w')
        r = requests.post(
            f'{host}{prefix}',
            json=new_shoes.dict(),
            headers=headers
        )
        shoes = shoes_schema.Shoes(**r.json())
        print(shoes)

    def test_case01_get(self):
        r = requests.get(f"{host}{prefix}/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = shoes_schema.Shoes(**r.json())
        self.assertEqual(shoes, shoes_schema.Shoes(id=self.prod_id, color='red', size=41, length=19, width='w'))

    def test_case01_get_all(self):
        r = requests.get(f"{host}{prefix}", headers=headers)
        self.assertEqual(r.status_code, 200)
        list_shoes = shoes_schema.ListShoes.parse_obj(r.json())
        shoes = list_shoes[-1]
        self.assertEqual(shoes, shoes_schema.Shoes(id=self.prod_id, color='red', size=41, length=19, width='w'))

    def test_case02_update(self):
        new_shoes = shoes_schema.UpdateShoes(color='blue', size=44, length=20, width='e')
        r = requests.put(
            f"{host}{prefix}/{self.prod_id}",
            json=new_shoes.dict(),
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}{prefix}/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = shoes_schema.Shoes(**r.json())
        self.assertEqual(shoes, shoes_schema.Shoes(id=self.prod_id, color='blue', size=44, length=20, width='e'))

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}{prefix}/{cls.prod_id}", headers=headers)
