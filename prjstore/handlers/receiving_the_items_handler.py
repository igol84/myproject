from prjstore.db import API_DB, schemas as db_schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.products.shoes_components import Width
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.receiving_the_items.schemas import ModelColorShoesShow, ModelProductShow, ModelSizeShoes, \
    ModelProductForm
from util.money import Money


class ReceivingTheItemsHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, store_id=1, test=False):
        self.__db = db
        self.test = test
        if test:
            self.__store = Store(id=store_id, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))

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

    def save_data(self, data: ModelProductForm):
        if data.type.name == 'product':
            if data.id:
                # create new item
                pd_item = db_schemas.item.CreateItem(prod_id=data.id, store_id=self.__store.id, qty=data.qty,
                                                     buy_price=data.price_buy)
                new_item = self.__db.item.create(pd_item)
                if new_item:
                    return True
            else:
                # create new product and item
                product = ProductFactory.create(name=data.name, price=Money(data.price_sell))
                new_product = ProductFactory.create_from_schema(self.__db.product.create(product.schema_create()))
                CreateRowProductCatalog = db_schemas.product_catalog.CreateRowProductCatalog
                pd_pc_row = CreateRowProductCatalog(store_id=self.__store.id, prod_id=new_product.prod_id)
                self.__db.product_catalog.create(pd_pc_row)
                pd_item = db_schemas.item.CreateItem(prod_id=new_product.prod_id, store_id=self.__store.id,
                                                     qty=data.qty, buy_price=data.price_buy)
                new_item = self.__db.item.create(pd_item)
                if new_item:
                    return True
        elif data.type.name == 'shoes':
            for size in data.module.sizes:
                result = self.find_shoes((data.name, data.module.color, data.module.width, size))
                if result:
                    print('create new item for product.shoes id:', result.prod_id)
                    qty = data.module.sizes[size].qty
                    pd_item = db_schemas.item.CreateItem(prod_id=result.prod_id, store_id=self.__store.id, qty=qty,
                                                         buy_price=data.price_buy)
                    new_item = self.__db.item.create(pd_item)
                    if new_item:
                        return True
                else:
                    # create new product.shoes and item
                    color = data.module.color
                    length = data.module.sizes[size].length
                    widths: dict[str, Width] = Shoes.widths
                    width = None
                    for _width in widths.values():
                        if _width.short_name == data.module.width:
                            width = _width

                    shoes = ProductFactory.create(product_type='shoes', name=data.name, price=Money(data.price_sell),
                                                  color=color, size=size, length_of_insole=length, width=width)
                    new_product = ProductFactory.create_from_schema(self.__db.product.create(shoes.schema_create()))
                    CreateRowProductCatalog = db_schemas.product_catalog.CreateRowProductCatalog
                    pd_pc_row = CreateRowProductCatalog(store_id=self.__store.id, prod_id=new_product.prod_id)
                    self.__db.product_catalog.create(pd_pc_row)
                    print(new_product)

    def find_shoes(self, keys):
        products: dict[str, AbstractProduct] = self.__store.pc.search(keys[0])
        for prod_id, prod in products.items():
            if prod.product_type == 'shoes':
                width = getattr(prod.width, 'short_name', '')
                if keys == (prod.name, prod.color, width, prod.size):
                    return products[prod_id]
        return False
