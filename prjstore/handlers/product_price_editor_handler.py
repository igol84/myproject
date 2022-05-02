from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import *
from prjstore.domain.item import Item
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.product_price_editor.schemas import create_product_schemas_by_items, ViewProduct


class ProductPriceEditorHandler:
    __main_handler: Optional[MainHandler]
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, main_handler=None):
        self.__main_handler = main_handler
        self.__db = db
        self.store_id = self.db.headers['store_id']
        self.test = test
        if test:
            self.__store = Store(id=self.store_id, name='test')
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

    def get_store_id(self):
        return self.store.id

    def get_store_products(self, search: Optional[str] = None) -> list[ViewProduct]:
        products: dict[int: Item] = self.store.items if not search else self.search_items(search)
        return create_product_schemas_by_items(products)

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        return self.store.search_items(value=text, fields={'name', 'prod_id'})

    def edit_product(self, data: ModelProductForm) -> ModelProductForm:
        # edit on DB
        new_data: ModelSizeForm = self.db.handler_product_price_editor.edit_product(data)
        # edit in Domain Model
        product = self.store.pc[data.id]
        if data.new_name is not None:
            product.name = data.new_name
        if data.new_price is not None:
            product.price.amount = data.new_price
        return new_data

    def edit_size(self, data: ModelSizeForm) -> ModelSizeForm:
        # edit on DB
        new_data: ModelSizeForm = self.db.handler_product_price_editor.edit_size(data)
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
        new_data: ModelShoesForm = self.db.handler_product_price_editor.edit_shoes(data)
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
        new_data: ModelShoesForm = self.db.handler_product_price_editor.edit_color(data)
        # edit in Domain Model
        products = self.store.pc.find(name=data.name, shoes={'color': data.color})
        for product in products:
            if data.new_color is not None:
                product.color = data.new_color
            if data.price_for_sale is not None:
                product.price.amount = data.price_for_sale
        return new_data
