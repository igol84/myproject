import unittest

from prjstore.db import API_DB, schemas
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from util.money import Money

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
        shoes = ProductFactory.create(product_type='shoes', prod_id='6', name='converse', price=Money(10),
                                      color='red', size=40, length_of_insole=25.5, width=Shoes.widths['Wide'])
        new_product = ProductFactory.create_from_schema(db.product.create(shoes.schema_create()))
        cls.obj_id = new_product.prod_id

    def test_case01_get(self):
        shoes = ProductFactory.create_from_schema(db.product.get(self.obj_id))
        self.assertEqual(shoes.name, 'converse')
        self.assertEqual(shoes.color, 'red')

    def test_case02_update(self):
        pd_shoes = schemas.shoes.CreateShoesWithProduct(color='white', size=40, length=25.5, width="Wide")
        pd_product = schemas.product.UpdateProduct(id=self.obj_id, type="shoes", name="nike", price=10, shoes=pd_shoes)
        product = ProductFactory.create_from_schema(db.product.update(pd_product))
        self.assertEqual(product.name, 'nike')
        self.assertEqual(product.color, 'white')

    @classmethod
    def tearDownClass(cls):
        db.product.delete(cls.obj_id)
