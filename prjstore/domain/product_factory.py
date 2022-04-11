from typing import overload, Literal, Optional

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.products.simple_product import SimpleProduct
from util.money import Money


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

    @staticmethod
    def create_from_schema(product_pd: schemas.product.Product):
        if product_pd.type == "shoes":
            width = Shoes.widths[product_pd.shoes.width] if product_pd.shoes.width else None
            product = ProductFactory.create(
                product_type=product_pd.type, prod_id=product_pd.id, name=product_pd.name,
                price=Money(product_pd.price),
                color=product_pd.shoes.color, size=product_pd.shoes.size,
                length_of_insole=product_pd.shoes.length, width=width)
        else:
            product = ProductFactory.create(
                product_type="product", prod_id=product_pd.id,
                name=product_pd.name, price=(product_pd.price,))
        return product
