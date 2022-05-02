from typing import Optional

from prjstore.db import API_DB
from prjstore.db.schemas import seller as db_schemas
from prjstore.domain.seller import Seller
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.sellers_editor import schemas


class SellersEditorHandler:
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

    def get_store_sellers(self) -> list[schemas.ViewSeller]:
        sellers: dict[int: Seller] = self.store.sellers
        list_pd_sellers = []
        for seller_id, seller in sellers.items():
            pd_seller = schemas.ViewSeller(seller_id=seller_id, name=seller.name, active=seller.active)
            list_pd_sellers.append(pd_seller)
            list_pd_sellers.sort(key=lambda k: k.seller_id, reverse=True)
        return list_pd_sellers

    def edit_name(self, seller_id: int, new_name: str):
        # edit on DB
        pd_seller: db_schemas.UpdateSeller = self.db.seller.edit_name(seller_id, new_name)
        # edit in Domain Model
        self.store.sellers[pd_seller.id].name = pd_seller.name
        return pd_seller

    def edit_active(self, seller_id: int, active: bool):
        # edit on DB
        pd_seller: db_schemas.UpdateSeller = self.db.seller.edit_active(seller_id, active)
        # edit in Domain Model
        self.store.sellers[pd_seller.id].active = pd_seller.active
        return pd_seller

    def add_seller(self, name: str):
        # edit on DB
        store_id = self.store_id
        pd_create_seller = db_schemas.CreateSeller(store_id=store_id, name=name, active=True)
        pd_seller: db_schemas.Seller = self.db.seller.create(pd_create_seller)
        # edit in Domain Model

        self.store.sellers[pd_seller.id] = Seller(id=pd_seller.id, name=pd_seller.name, active=pd_seller.active)
        return pd_seller
