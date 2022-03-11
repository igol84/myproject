from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import *
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

    def get_store_products(self, search: Optional[str] = None) -> list[ViewProduct]:
        products: dict[int: Item] = self.store.items if not search else self.search_items(search)
        return create_product_schemas_by_items(products)

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        return self.store.search_items(value=text, fields={'name', 'prod_id'})

    def edit_size(self, data: ModelSize) -> ModelSize:
        # edit on DB
        new_data: ModelSize = self.__db.handler_product_price_editor.edit_size(data)
        # edit in Domain Model
        sizes = self.store.get_items_by_pr_id(data.id)
        for size in sizes:
            size.product.price.amount = data.price_for_sale
            size.product.size = data.size
        return new_data

    def edit_shoes(self, data: ModelShoes) -> ModelShoes:
        # edit on DB
        new_data: ModelShoes = self.__db.handler_product_price_editor.edit_shoes(data)
        # edit in Domain Model
        list_shoes = self.store.get_items_by_pr_name(data.name)
        for shoes in list_shoes:
            shoes.product.name = data.new_name
            shoes.product.price.amount = data.price_for_sale
        return new_data

    def edit_color(self, data: ModelColor) -> ModelColor:
        # edit on DB
        new_data: ModelShoes = self.__db.handler_product_price_editor.edit_color(data)
        # edit in Domain Model
        list_shoes = self.store.get_items_by_name_and_color(data.name, data.color)
        for shoes in list_shoes:
            shoes.product.color = data.new_color
            shoes.product.price.amount = data.price_for_sale
        return new_data
