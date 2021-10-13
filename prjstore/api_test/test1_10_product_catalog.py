import unittest
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.db import API_DB
from prjstore.db.schemas import product_catalog as schemas

count_rows = 0
db = API_DB()


def setUpModule():
    product_catalog = db.product_catalog.get_all()
    global count_rows
    count_rows = len(product_catalog)


def tearDownModule():
    product_catalog = db.product_catalog.get_all()
    global count_rows
    assert count_rows == len(product_catalog), f" count product_catalog changed '"


class TestProductCatalog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pd_pc_row = schemas.CreateRowProductCatalog(store_id=1, prod_id=3)
        db.product_catalog.create(pd_pc_row)

    def test_case01_get(self):
        self.assertEqual(db.product_catalog.check(store_id=1, prod_id=3), True)

    def test_case02_get_pc(self):
        pc_pd = db.product_catalog.get_store_pc(store_id=1)
        pc = ProductCatalog.create_from_schema(pc_pd)
        self.assertEqual(list(pc.products.keys())[-1], '3')

    @classmethod
    def tearDownClass(cls):
        db.product_catalog.delete(store_id=1, prod_id=3)
