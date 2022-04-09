from prjstore.db import API_DB, schemas
from prjstore.domain.place_of_sale import PlaceOfSale

count_rows = 0
db = API_DB()


def setup_method():
    places: list = db.place.get_all()
    global count_rows
    count_rows = len(places)


def teardown_method():
    places = db.place.get_all()
    global count_rows
    assert count_rows == len(places), f" count place changed '"


class TestPlace:
    obj_id: int = None

    @classmethod
    def setup_class(cls):
        pd_place = schemas.place.CreatePlace(store_id=1, name="Место", active=True)
        new_place = PlaceOfSale.create_from_schema(db.place.create(pd_place))
        cls.obj_id = new_place.id

    def test_case01_get(self):
        place = PlaceOfSale.create_from_schema(db.place.get(self.obj_id))
        assert place.name == 'Место'

    def test_case02_update(self):
        pd_place = schemas.place.UpdatePlace(id=self.obj_id, store_id=1, name="Точка", active=True)
        place = PlaceOfSale.create_from_schema(db.place.update(pd_place))
        assert place.name == 'Точка'

    @classmethod
    def teardown_class(cls):
        db.place.delete(cls.obj_id)
