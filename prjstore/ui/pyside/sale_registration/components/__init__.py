from typing import overload, Optional, Literal

from pydantic import validate_arguments

from prjstore.ui.pyside.sale_registration.components.simple_product import ProductFrame
from prjstore.ui.pyside.sale_registration.components.shoes import ShoesFrame




class FrameItemFactory:

    @overload
    @staticmethod
    def create(product_type: Optional[Literal['product']], *args, **kwargs) -> ProductFrame:
        ...

    @overload
    @staticmethod
    def create(product_type: Literal['shoes'], *args, **kwargs) -> ShoesFrame:
        ...

    @staticmethod
    @validate_arguments
    def create(product_type: Literal['product', 'shoes'] = 'product', *args, **kwargs):
        products = {
            'product': ProductFrame,
            'shoes': ShoesFrame,
        }
        return products[product_type](*args, **kwargs)
