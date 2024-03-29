from prjstore.db import API_DB, schemas
from prjstore.domain.product_factory import ProductFactory
from util.money import Money

count_rows = 0
db = API_DB({'username': '', 'password': ''})


def setup_method():
    products: list = db.product.get_all()
    global count_rows
    count_rows = len(products)


def teardown_method():
    products = db.product.get_all()
    global count_rows
    assert count_rows == len(products), f" count product changed '"


class TestProduct:
    obj_id: int = None

    @classmethod
    def setup_class(cls):
        product = ProductFactory.create(name='book', price=Money('10'))
        new_product = ProductFactory.create_from_schema(db.product.create(product.schema_create()))
        cls.obj_id = new_product.prod_id

    def test_case01_get(self):
        product = ProductFactory.create_from_schema(db.product.get(self.obj_id))
        assert product.name == 'book'

    def test_case02_update(self):
        pd_product = schemas.product.Product(id=self.obj_id, type="", name="dog", price=10)
        product = ProductFactory.create_from_schema(db.product.update(pd_product))
        assert product.name == 'dog'

    @classmethod
    def teardown_class(cls):
        db.product.delete(cls.obj_id)
