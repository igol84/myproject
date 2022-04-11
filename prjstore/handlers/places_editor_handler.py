from prjstore.db import API_DB
from prjstore.db.schemas import place as db_schemas
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.places_editor import schemas


class PlacesEditorHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, store=None):
        self.__db = db
        if test:
            self.__store = Store(id=1, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.store_id = db.headers['store_id']
            self.update_data(store)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def update_data(self, store: Store):
        if not store:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))
        else:
            self.__store = store

    def get_store_places(self) -> list[schemas.ViewPlace]:
        places: dict[int: PlaceOfSale] = self.__store.places_of_sale
        list_pd_places = []
        for place_id, place in places.items():
            pd_place = schemas.ViewPlace(place_id=place_id, name=place.name, active=place.active)
            list_pd_places.append(pd_place)
            list_pd_places.sort(key=lambda k: k.place_id, reverse=True)
        return list_pd_places

    def edit_name(self, place_id: int, new_name: str):
        # edit on DB
        pd_place: db_schemas.UpdatePlace = self.__db.place.edit_name(place_id, new_name)
        # edit in Domain Model
        self.store.places_of_sale[pd_place.id].name = pd_place.name
        return pd_place

    def edit_active(self, place_id: int, active: bool):
        # edit on DB
        pd_place: db_schemas.UpdatePlace = self.__db.place.edit_active(place_id, active)
        # edit in Domain Model
        self.store.places_of_sale[pd_place.id].active = pd_place.active
        return pd_place

    def add_place(self, name: str):
        # edit on DB
        store_id = self.store_id
        pd_create_place = db_schemas.CreatePlace(store_id=store_id, name=name, active=True)
        pd_place: db_schemas.Place = self.__db.place.create(pd_create_place)
        # edit in Domain Model

        self.store.places_of_sale[pd_place.id] = PlaceOfSale(id=pd_place.id, name=pd_place.name, active=pd_place.active)
        return pd_place
