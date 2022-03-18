from prjstore.db import API_DB
from prjstore.domain.store import Store


class MainHandler:
    __store: Store

    def __init__(self, db: API_DB):
        self.__db = db
        self.update_data()

    def get_store(self) -> Store:
        return self.__store

    def set_store(self, store: Store) -> None:
        self.__store = store

    store = property(get_store, set_store)

    def update_data(self, store=None):
        if not store:
            store_id = self.__db.headers['store_id']
            self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))
        else:
            self.__store = store