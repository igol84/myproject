import unittest
from prjstore.db import API_DB, schemas
from prjstore.domain.store import Store

count_rows = 0
db = API_DB()


def setUpModule():
    stores: list = db.store.get_all()
    global count_rows
    count_rows = len(stores)


def tearDownModule():
    stores = db.store.get_all()
    global count_rows
    assert count_rows == len(stores), f" count store changed '"


class TestStore(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        pd_store = schemas.store.CreateStore(name="маг1", desc='')
        new_store = Store.create_from_schema(db.store.create(pd_store))
        cls.obj_id = new_store.id

    def test_case01_get(self):
        store = Store.create_from_schema(db.store.get(self.obj_id))
        self.assertEqual(store.name, 'маг1')

    def test_case02_update(self):
        pd_store = schemas.store.UpdateStore(id=self.obj_id, name="маг2", desc='')
        store = Store.create_from_schema(db.store.update(pd_store))
        self.assertEqual(store.name, 'маг2')

    @classmethod
    def tearDownClass(cls):
        db.store.delete(cls.obj_id)
