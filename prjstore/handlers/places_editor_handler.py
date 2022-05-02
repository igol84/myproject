from typing import Optional

from prjstore.db import API_DB
from prjstore.db.schemas import place as db_schemas
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.places_editor import schemas


class PlacesEditorHandler:
    __main_handler: Optional[MainHandler]
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, main_handler=None):
        self.__main_handler = main_handler
        self.__db = db
        self.store_id = self.db.headers['store_id']
        if test:
            self.__store = Store(id=1, name='test')
            put_test_data_to_store(self.__store)
        if not main_handler:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))

    def __get_main_handler(self) -> Optional[MainHandler]:
        return self.__main_handler

    def __set_main_handler(self, main_handler: MainHandler) -> None:
        self.__main_handler = main_handler

    main_handler = property(__get_main_handler, __set_main_handler)

    def __get_store(self):
        if self.main_handler:
            store = self.main_handler.store
        else:
            store = self.__store
        return store

    store = property(__get_store)

    def __get_db(self):
        if self.main_handler:
            db = self.main_handler.db
        else:
            db = self.__db
        return db

    db = property(__get_db)

    def get_store_places(self) -> list[schemas.ViewPlace]:
        places: dict[int: PlaceOfSale] = self.store.places_of_sale
        list_pd_places = []
        for place_id, place in places.items():
            pd_place = schemas.ViewPlace(place_id=place_id, name=place.name, active=place.active)
            list_pd_places.append(pd_place)
            list_pd_places.sort(key=lambda k: k.place_id, reverse=True)
        return list_pd_places

    def edit_name(self, place_id: int, new_name: str):
        # edit on DB
        pd_place: db_schemas.UpdatePlace = self.db.place.edit_name(place_id, new_name)
        # edit in Domain Model
        self.store.places_of_sale[pd_place.id].name = pd_place.name
        return pd_place

    def edit_active(self, place_id: int, active: bool):
        # edit on DB
        pd_place: db_schemas.UpdatePlace = self.db.place.edit_active(place_id, active)
        # edit in Domain Model
        self.store.places_of_sale[pd_place.id].active = pd_place.active
        return pd_place

    def add_place(self, name: str):
        # edit on DB
        store_id = self.store_id
        pd_create_place = db_schemas.CreatePlace(store_id=store_id, name=name, active=True)
        pd_place: db_schemas.Place = self.db.place.create(pd_create_place)
        # edit in Domain Model

        self.store.places_of_sale[pd_place.id] = PlaceOfSale(id=pd_place.id, name=pd_place.name, active=pd_place.active)
        return pd_place
