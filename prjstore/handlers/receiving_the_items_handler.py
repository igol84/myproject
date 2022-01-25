from prjstore.db import API_DB
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.receiving_the_items.schemas import ModelProduct, ModelColorShoes, ModelSizeShoes


class ReceivingTheItemsHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, store_id=1, test=False):
        self.__db = db
        self.test_mode = test
        if test:
            self.__store = Store(id=store_id, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.__store = Store.create_from_schema(self.__db.store.get(id=store_id))

    def get_products_data(self) -> list[ModelProduct]:

        return self.convert_pc_to_pd_model()

    def convert_pc_to_pd_model(self) -> list[ModelProduct]:
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
                    module = ModelColorShoes(color=color, width=width, sizes=sizes)
                pd_prod = ModelProduct(id=prod.prod_id, type=prod.product_type, name=prod.name,
                                       price_sell=prod.price.amount, module=module)
                pd_products[key] = pd_prod
            else:
                if prod.product_type == 'shoes':
                    model_shoes = ModelSizeShoes(size=prod.size, length=prod.length_of_insole)
                    pd_products[key].module.sizes[prod.size] = model_shoes
        return [pr for pr in pd_products.values()]


def get_test_data() -> list[ModelProduct]:
    list_pd_prod = []
    sizes = {38: ModelSizeShoes(size=38, length=24.5, qty=5), 39: ModelSizeShoes(size=39, length=25, qty=8),
             42: ModelSizeShoes(size=42, length=27.5, qty=1), 43: ModelSizeShoes(size=43, length=28, qty=2)}
    shoes = ModelColorShoes(color='black', width='EE', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=115, type='shoes', name='con chak h 70', price_sell=640.40, module=shoes))
    list_pd_prod.append(ModelProduct(id=22, type='product', name='battery', price_sell=840))
    for n in range(23, 24):
        list_pd_prod.append(ModelProduct(id=n, type='product', name=f'battery {n}', price_sell=840 + n))
    sizes = {36: ModelSizeShoes(size=36, length=23.5, qty=1), 37: ModelSizeShoes(size=37, length=24, qty=2),
             38: ModelSizeShoes(size=38, length=24.5, qty=1), 39: ModelSizeShoes(size=39, length=25, qty=2),
             41: ModelSizeShoes(size=41, length=26.5, qty=3)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 70', price_sell=420, module=shoes))

    sizes = {37: ModelSizeShoes(size=37, length=24, qty=1), 38: ModelSizeShoes(size=38, length=24.5, qty=2),
             39: ModelSizeShoes(size=39, length=25, qty=1), 40: ModelSizeShoes(size=40, length=25.5, qty=2)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 75', price_sell=425, module=shoes))
    return list_pd_prod
