from prjstore.db import API_DB, schemas as db_schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.item import Item
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.product_price_editor.schemas import create_product_schemas_by_items, ViewProduct


class ProductPriceEditor:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False):
        self.__db = db
        self.store_id = db.headers['store_id']
        self.test = test
        if test:
            self.__store = Store(id=self.store_id, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))

    def get_store(self):
        return self.__store

    store = property(get_store)

    def get_store_id(self):
        return self.__store.id

    def get_store_products(self) -> list[ViewProduct]:
        products: dict[int: Item] = self.store.items
        return create_product_schemas_by_items(products)

    def save_data(self, data: db_schemas.header_receiving_the_items.ModelProduct):
        data.store_id = self.__store.id
        return self.__db.header_receiving_the_items.receiving_the_items(data)

    def find_shoes(self, keys):
        products: dict[str, AbstractProduct] = self.__store.pc.search(keys[0])
        for prod_id, prod in products.items():
            if prod.product_type == 'shoes':
                width = getattr(prod.width, 'short_name', '')
                if keys == (prod.name, prod.color, width, prod.size):
                    return products[prod_id]
        return False
