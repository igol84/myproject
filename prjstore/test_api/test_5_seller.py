from prjstore.db import API_DB, schemas
from prjstore.domain.seller import Seller

count_rows = 0
db = API_DB()


def setup_method():
    sellers: list = db.seller.get_all()
    global count_rows
    count_rows = len(sellers)


def teardown_method():
    sellers = db.seller.get_all()
    global count_rows
    assert count_rows == len(sellers), f" count seller changed '"


class TestSeller:
    obj_id: int = None

    @classmethod
    def setup_class(cls):
        pd_seller = schemas.seller.CreateSeller(store_id=1, name="Igor")
        new_seller = Seller.create_from_schema(db.seller.create(pd_seller))
        cls.obj_id = new_seller.id

    def test_case01_get(self):
        seller = Seller.create_from_schema(db.seller.get(self.obj_id))
        assert seller.name == 'Igor'

    def test_case02_update(self):
        pd_seller = schemas.seller.UpdateSeller(id=self.obj_id, store_id=1, name="Anna")
        seller = Seller.create_from_schema(db.seller.update(pd_seller))
        assert seller.name == 'Anna'

    @classmethod
    def teardown_class(cls):
        db.seller.delete(cls.obj_id)
