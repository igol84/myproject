import unittest
from prjstore.db import API_DB, schemas
from prjstore.domain.place_of_sale import PlaceOfSale

count_rows = 0
db = API_DB()


def setUpModule():
    places: list = db.place.get_all()
    global count_rows
    count_rows = len(places)


def tearDownModule():
    places = db.place.get_all()
    global count_rows
    assert count_rows == len(places), f" count place changed '"


class TestPlace(unittest.TestCase):
    obj_id: int = None

    @classmethod
    def setUpClass(cls):
        pd_place = schemas.place.CreatePlace(store_id=1, name="Место")
        new_place = PlaceOfSale.create_from_schema(db.place.create(pd_place))
        cls.obj_id = new_place.id

    def test_case01_get(self):
        place = PlaceOfSale.create_from_schema(db.place.get(self.obj_id))
        self.assertEqual(place.name, 'Место')

    def test_case02_update(self):
        pd_place = schemas.place.UpdatePlace(id=self.obj_id, store_id=1, name="Точка")
        place = PlaceOfSale.create_from_schema(db.place.update(pd_place))
        self.assertEqual(place.name, 'Точка')

    @classmethod
    def tearDownClass(cls):
        db.place.delete(cls.obj_id)
