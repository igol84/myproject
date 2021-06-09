from typing import overload, Literal, Optional

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.products.simple_product import SimpleProduct
from prjstore.domain.products.shoes import Shoes


@dataclass
class ProductFactory:

    @overload
    @staticmethod
    def create(product_type: Optional[Literal['product']], *args, **kwargs) -> SimpleProduct:
        ...

    @overload
    @staticmethod
    def create(product_type: Literal['shoes'], *args, **kwargs) -> Shoes:
        ...

    @staticmethod
    @validate_arguments
    def create(product_type: Literal['product', 'shoes'] = 'product', *args, **kwargs):
        products = {
            'product': SimpleProduct,
            'shoes': Shoes,
        }
        return products[product_type](*args, **kwargs)
