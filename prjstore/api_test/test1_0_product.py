import unittest

from prjstore.db import API_DB, schemas
from prjstore.domain.product_factory import ProductFactory

count_rows = 0
db = API_DB()


def setUpModule():
    products: list = db.product.get_all()
    global count_rows
    count_rows = len(products)


def tearDownModule():
    products = db.product.get_all()
    global count_rows
    assert count_rows == len(products), f" count product changed '"


class TestProduct(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        pd_product = schemas.product.CreateProduct(type="", name="book", price=10)
        new_product = ProductFactory.create_from_schema(db.product.create(pd_product))
        cls.obj_id = new_product.prod_id

    def test_case01_get(self):
        product = ProductFactory.create_from_schema(db.product.get(self.obj_id))
        self.assertEqual(product.name, 'book')

    def test_case02_update(self):
        pd_product = schemas.product.Product(id=self.obj_id, type="", name="dog", price=10)
        product = ProductFactory.create_from_schema(db.product.update(pd_product))
        self.assertEqual(product.name, 'dog')

    @classmethod
    def tearDownClass(cls):
        db.product.delete(cls.obj_id)
