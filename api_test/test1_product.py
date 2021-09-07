import unittest
import requests
from api_test.authorization import host, headers
from prjstore.schemas import product as product_schema
from prjstore.schemas import shoes as shoes_schema

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
        self.assertEqual(product.type, '')
        self.assertEqual(product.name, 'battery')
        self.assertEqual(product.price, 10)

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
        self.assertEqual(product.type, 'shoes')
        self.assertEqual(product.name, 'converse')
        self.assertEqual(product.price, 15)

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}{prefix}/{cls.prod_id}", headers=headers)


class TestShoes(unittest.TestCase):
    prod_id: int = None

    @classmethod
    def setUpClass(cls):
        new_product = product_schema.CreateProduct(type="shoes", name="converse", price=10)
        r = requests.post(
            f'{host}{prefix}/',
            json=new_product.dict(),
            headers=headers
        )
        product = product_schema.Product(**r.json())
        print(product)
        cls.prod_id = product.id
        new_shoes = shoes_schema.CreateShoes(id=product.id, color='red', size=41, length=19, width='w')
        r = requests.post(
            f'{host}/shoes/',
            json=new_shoes.dict(),
            headers=headers
        )
        shoes = shoes_schema.Shoes(**r.json())
        print(shoes)

    def test_case01_get(self):
        r = requests.get(f"{host}/shoes/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = shoes_schema.Shoes(**r.json())
        self.assertEqual(shoes.color, 'red')
        self.assertEqual(shoes.size, 41)
        self.assertEqual(shoes.length, 19)
        self.assertEqual(shoes.width, 'w')

    def test_case02_update(self):
        new_shoes = shoes_schema.UpdateShoes(color='blue', size=44, length=20, width='e')
        r = requests.put(
            f"{host}/shoes/{self.prod_id}",
            json=new_shoes.dict(),
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}/shoes/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = shoes_schema.Shoes(**r.json())
        self.assertEqual(shoes.color, 'blue')
        self.assertEqual(shoes.size, 44)
        self.assertEqual(shoes.length, 20)
        self.assertEqual(shoes.width, 'e')

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}/shoes/{cls.prod_id}", headers=headers)
