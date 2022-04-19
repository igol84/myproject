from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import *
from prjstore.domain.item import Item
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.product_price_editor.schemas import create_product_schemas_by_items, ViewProduct


class ProductPriceEditorHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, store=None):
        self.__db = db
        self.store_id = db.headers['store_id']
        self.test = test
        if test:
            self.__store = Store(id=self.store_id, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.update_data(store)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def update_data(self, store: Store):
        if not store:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))
        else:
            self.__store = store

    def get_store_id(self):
        return self.__store.id

    def get_store_products(self, search: Optional[str] = None) -> list[ViewProduct]:
        products: dict[int: Item] = self.store.items if not search else self.search_items(search)
        return create_product_schemas_by_items(products)

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        return self.store.search_items(value=text, fields={'name', 'prod_id'})

    def edit_product(self, data: ModelProductForm) -> ModelProductForm:
        # edit on DB
        new_data: ModelSizeForm = self.__db.handler_product_price_editor.edit_product(data)
        # edit in Domain Model
        product = self.store.pc[data.id]
        if data.new_name is not None:
            product.name = data.new_name
        if data.new_price is not None:
            product.price.amount = data.new_price
        return new_data

    def edit_size(self, data: ModelSizeForm) -> ModelSizeForm:
        # edit on DB
        new_data: ModelSizeForm = self.__db.handler_product_price_editor.edit_size(data)
        # edit in Domain Model
        product: Shoes = self.store.pc[data.id]
        if data.price_for_sale is not None:
            product.price.amount = data.price_for_sale
        if data.size is not None:
            product.size = data.size
        if data.length is not None:
            product.length_of_insole = data.length
        return new_data

    def edit_shoes(self, data: ModelShoesForm) -> ModelShoesForm:
        # edit on DB
        new_data: ModelShoesForm = self.__db.handler_product_price_editor.edit_shoes(data)
        # edit in Domain Model
        products = self.store.pc.find(name=data.name)
        for product in products:
            if data.new_name is not None:
                product.name = data.new_name
            if data.price_for_sale is not None:
                product.price.amount = data.price_for_sale
        return new_data

    def edit_color(self, data: ModelColorForm) -> ModelColorForm:
        # edit on DB
        new_data: ModelShoesForm = self.__db.handler_product_price_editor.edit_color(data)
        # edit in Domain Model
        products = self.store.pc.find(name=data.name, shoes={'color': data.color})
        for product in products:
            if data.new_color is not None:
                product.color = data.new_color
            if data.price_for_sale is not None:
                product.price.amount = data.price_for_sale
        return new_data
