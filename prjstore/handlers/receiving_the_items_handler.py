from prjstore.db import API_DB, schemas as db_schemas
from prjstore.db.schemas import handler_receiving_the_items as db_schema
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.item import Item
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.store import Store
from prjstore.handlers.abstract_module_handler import AbstractModuleHandler
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.receiving_the_items import schemas


class ReceivingTheItemsHandler(AbstractModuleHandler):
    db: API_DB
    store: Store

    def __init__(self, db: API_DB = None, main_handler: MainHandler = None):
        super().__init__(db, main_handler)

    @staticmethod
    def get_shoes_widths():
        return ((width_name, getattr(width, 'short_name', '')) for width_name, width in Shoes.widths.items())

    def get_products_data(self) -> list[schemas.ModelProductShow]:
        # return get_test_data()
        return self.convert_pc_to_pd_model_show()

    def convert_pc_to_pd_model_show(self) -> list[schemas.ModelProductShow]:
        prods: dict[str, AbstractProduct] = self.store.pc.products
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
                    sizes = {prod.size: schemas.ModelSizeShoes(size=prod.size, length=prod.length_of_insole)}
                    module = schemas.ModelColorShoesShow(colors=[color], width=width, sizes=sizes)
                pd_prod = schemas.ModelProductShow(id=prod.prod_id, type=prod.product_type, name=prod.name,
                                                   price_sell=prod.price.amount, module=module)
                pd_products[key] = pd_prod
            else:
                if prod.product_type == 'shoes':
                    model_shoes = schemas.ModelSizeShoes(size=prod.size, length=prod.length_of_insole)
                    pd_products[key].module.sizes[prod.size] = model_shoes
                    pd_products[key].module.colors.add(color)
        return [pr for pr in pd_products.values()]

    def save_data(self, data: db_schemas.handler_receiving_the_items.ModelProduct) -> None:
        data.store_id = self.store.id
        output_items: db_schema.OutputItems = self.db.header_receiving_the_items.receiving_the_items(data)
        pd_products = output_items.products
        pd_items = output_items.items
        for pd_product in pd_products:
            product = ProductFactory.create_from_schema(pd_product)
            self.store.pc.set_product(product)

        for pd_item in pd_items:
            product = self.store.pc[pd_item.prod_id]
            item = Item.create_from_schema_with_product(pd_item, product)
            self.store.set_item(item)

    def find_shoes(self, keys):
        products: dict[str, AbstractProduct] = self.store.pc.search(keys[0])
        for prod_id, prod in products.items():
            if prod.product_type == 'shoes':
                width = getattr(prod.width, 'short_name', '')
                if keys == (prod.name, prod.color, width, prod.size):
                    return products[prod_id]
        return False
