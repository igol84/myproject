from prjstore.db import API_DB
from prjstore.domain.store import Store


class MainHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB):
        self.__db = db
        store_id = self.__db.headers['store_id']
        self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))

    def __get_db(self) -> API_DB:
        return self.__db

    db = property(__get_db)

    def __get_store(self) -> Store:
        return self.__store

    store = property(__get_store)
