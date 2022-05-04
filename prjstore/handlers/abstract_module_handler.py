from typing import Optional

from prjstore.db import API_DB
from prjstore.domain.store import Store
from prjstore.handlers.main_handler import MainHandler


class AbstractModuleHandler:
    __main_handler: Optional[MainHandler]
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, main_handler: MainHandler = None):
        self.__main_handler = main_handler
        self.__db = db
        if not main_handler and db:
            store_id = self.db.headers['store_id']
            self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))

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
