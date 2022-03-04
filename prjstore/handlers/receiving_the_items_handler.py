from prjstore.db import API_DB, schemas as db_schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.receiving_the_items.schemas import ModelColorShoesShow, ModelProductShow, ModelSizeShoes


class ReceivingTheItemsHandler:
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

    def get_store_id(self):
        return self.__store.id

    @staticmethod
    def get_shoes_widths():
        return ((width_name, getattr(width, 'short_name', '')) for width_name, width in Shoes.widths.items())

    def get_products_data(self) -> list[ModelProductShow]:
        # return get_test_data()
        return self.convert_pc_to_pd_model_show()

    def convert_pc_to_pd_model_show(self) -> list[ModelProductShow]:
        prods: dict[str, AbstractProduct] = self.__store.pc.products
        pd_products = {}
        sorted_products = sorted(prods.values(), key=lambda k: k.prod_id)
        for prod in sorted_products:
            color = getattr(prod, 'color', None)
            width_type = getattr(prod, 'width', None)
            width = getattr(width_type, 'name', None)
            key = prod.name
            if key not in pd_products:
                module = None
                if prod.product_type == 'shoes':
                    sizes = {prod.size: ModelSizeShoes(size=prod.size, length=prod.length_of_insole)}
                    module = ModelColorShoesShow(colors=[color], width=width, sizes=sizes)
                pd_prod = ModelProductShow(id=prod.prod_id, type=prod.product_type, name=prod.name,
                                           price_sell=prod.price.amount, module=module)
                pd_products[key] = pd_prod
            else:
                if prod.product_type == 'shoes':
                    model_shoes = ModelSizeShoes(size=prod.size, length=prod.length_of_insole)
                    pd_products[key].module.sizes[prod.size] = model_shoes
                    pd_products[key].module.colors.add(color)
        return [pr for pr in pd_products.values()]

    def save_data(self, data: db_schemas.handler_receiving_the_items.ModelProduct):
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
