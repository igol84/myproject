from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import *
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.item import Item
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.product_price_editor.schemas import create_product_schemas_by_items, ViewProduct


class ProductPriceEditorHandler:
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

    def edit_product(self, data: ModelProduct) -> ModelProduct:
        new_data: ModelProduct = self.__db.handler_product_price_editor.edit_product(data)
        return new_data

    def edit_shoes(self, data: ModelShoes) -> ModelShoes:
        new_data: ModelShoes = self.__db.handler_product_price_editor.edit_shoes(data)
        return new_data

    def edit_color(self, data: ModelColor) -> ModelColor:
        new_data: ModelShoes = self.__db.handler_product_price_editor.edit_color(data)
        return new_data

    def find_shoes(self, keys):
        products: dict[str, AbstractProduct] = self.__store.pc.search(keys[0])
        for prod_id, prod in products.items():
            if prod.product_type == 'shoes':
                width = getattr(prod.width, 'short_name', '')
                if keys == (prod.name, prod.color, width, prod.size):
                    return products[prod_id]
        return False
