from typing import Union, Optional

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes_components import Width
from util.money import Money


@dataclass
class Shoes(AbstractProduct):
    widths = {
        None: None,
        'Medium': Width(name='Medium', short_name='D', width_of_insole=10),
        'Wide': Width(name='Wide', short_name='EE', width_of_insole=12),
        'Extra Wide': Width(name='Extra Wide', short_name='4E', width_of_insole=13)
    }
    product_type: str = 'shoes'
    color: Optional[str] = None
    size: float = None
    length_of_insole: Optional[float] = None
    width: Optional[Width] = None

    ###############################################################################################
    def str_width(self):
        return getattr(self.width, 'name', '')

    @validate_arguments
    def edit(self,
             name: str = None,
             price: Union[Money, float] = None,
             currency: Optional[str] = None,
             color: str = None,
             size: float = None,
             length_of_insole: float = None,
             width: Union[Width, str] = None
             ) -> None:
        AbstractProduct.edit(self, name, price, currency)
        if color:
            self.color = str(color)
        if size:
            self.size = float(size)
        if length_of_insole:
            self.length_of_insole = float(length_of_insole)
        if width:
            if isinstance(width, Width):
                self.width = width
            elif isinstance(width, str) and width in Shoes.widths:
                self.width = Shoes.widths[width]
            else:
                raise ValueError('Dont find width: ', width)

    def schema_create(self) -> schemas.product.Product:
        shoes = schemas.shoes.Shoes(id=self.prod_id, color=self.color, size=self.size, length=self.length_of_insole,
                                    width=self.str_width())
        return super().schema_create(shoes=shoes)

    def copy(self, prod_id=None) -> 'Shoes':
        return Shoes(prod_id=prod_id, product_type=self.product_type, name=self.name, price=self.price,
                     color=self.color, size=self.size, length_of_insole=self.length_of_insole, width=self.width)
