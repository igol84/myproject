import unittest
import requests
from api_test.authorization import host, headers

count_rows = 0


def setUpModule():
    r = requests.get(f"{host}/prod", headers=headers)
    global count_rows
    count_rows = len(r.json())


def tearDownModule():
    r = requests.get(f"{host}/prod", headers=headers)
    global count_rows
    assert count_rows == len(r.json()), f" count prod changed '"


class TestProd(unittest.TestCase):
    prod_id: int = None

    @classmethod
    def setUpClass(cls):
        r = requests.post(
            f'{host}/prod/',
            json={"type": "", "name": "battery", "price": 10},
            headers=headers
        )
        cls.prod_id = r.json()['id']

    def test_case01_get(self):
        r = requests.get(f"{host}/prod/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        prod = r.json()
        self.assertEqual(prod['type'], '')
        self.assertEqual(prod['name'], 'battery')
        self.assertEqual(prod['price'], 10)

    def test_case02_update(self):
        r = requests.put(
            f"{host}/prod/{self.prod_id}",
            json={"type": "shoes", "name": "converse", "price": 15},
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}/prod/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        prod = r.json()
        self.assertEqual(prod['type'], 'shoes')
        self.assertEqual(prod['name'], 'converse')
        self.assertEqual(prod['price'], 15)

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}/prod/{cls.prod_id}", headers=headers)


class TestShoes(unittest.TestCase):
    prod_id: int = None

    @classmethod
    def setUpClass(cls):
        r = requests.post(
            f'{host}/prod/',
            json={"type": "shoes", "name": "converse", "price": 10},
            headers=headers
        )
        cls.prod_id = r.json()['id']
        requests.post(
            f'{host}/shoes/',
            json={"id": r.json()['id'], "color": "red", "size": 41, "length": 19, "width": "w"},
            headers=headers
        )

    def test_case01_get(self):
        r = requests.get(f"{host}/shoes/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = r.json()
        self.assertEqual(shoes['color'], 'red')
        self.assertEqual(shoes['size'], 41)
        self.assertEqual(shoes['length'], 19)
        self.assertEqual(shoes['width'], 'w')

    def test_case02_update(self):
        r = requests.put(
            f"{host}/shoes/{self.prod_id}",
            json={"color": "blue", "size": 44, "length": 20, "width": "e"},
            headers=headers
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"{host}/shoes/{self.prod_id}", headers=headers)
        self.assertEqual(r.status_code, 200)
        shoes = r.json()
        self.assertEqual(shoes['color'], 'blue')
        self.assertEqual(shoes['size'], 44)
        self.assertEqual(shoes['length'], 20)
        self.assertEqual(shoes['width'], 'e')

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"{host}/shoes/{cls.prod_id}", headers=headers)
