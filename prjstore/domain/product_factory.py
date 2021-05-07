from .abstract_product import AbstractProduct
from .products.simple_product import SimpleProduct
from .products.shoes import Shoes


class ProductFactory:

    @staticmethod
    def create(product_type='product', *args, **kwargs) -> AbstractProduct:
        products = {
            'product': SimpleProduct,
            'shoes': Shoes,
        }
        return products[product_type](*args, **kwargs)
