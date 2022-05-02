from prjstore.db import API_DB
from prjstore.domain.store import Store


class MainHandler:
    __store: Store

    def __init__(self, db: API_DB):
        self.__db = db
        store_id = self.__db.headers['store_id']
        self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))

    def get_db(self) -> API_DB:
        return self.__db

    db = property(get_db)

    def get_store(self) -> Store:
        return self.__store

    def set_store(self, store: Store) -> None:
        self.__store = store

    store = property(get_store, set_store)
