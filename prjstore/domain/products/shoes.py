import dataclasses
from decimal import Decimal
from typing import Union, Optional

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes_components import Width
from util.money import Money


@dataclass
class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(prod_id='6', name='nike air force', price=Money(900), color='red', \
size=43, width=Shoes.widths['Wide'], length_of_insole=28.5) # Create product
>>> tuple_data = dataclasses.astuple(shoes)
>>> tuple_data
('6', 'shoes', 'nike air force', (900.0, ('UAH', 27.5, '₴')), 'red', 43.0, 28.5, ('Wide', 'EE'))
>>> shoes2 = Shoes(*tuple_data)
>>> print(shoes2.name)
nike air force
>>> shoes.color='black'
>>> shoes.color
'black'

>>> shoes.size=44.
>>> shoes.size
44.0

>>> shoes.length_of_insole=28.0
>>> shoes.length_of_insole
28.0


>>> shoes.width = Shoes.widths['Medium']
>>> shoes.width.name
'Medium'
>>> shoes.width.short_name
'D'

>>> shoes.edit(name='nike air', price=500, color='red', size='42', \
width='Wide', length_of_insole=28.5)      # Edit product
>>> shoes.price.amount, shoes.color, shoes.size, shoes.width.name, shoes.length_of_insole
(500.0, 'red', 42.0, 'Wide', 28.5)
"""

    widths = {
        'Medium': Width(name='Medium', short_name='D'),
        'Wide': Width(name='Wide', short_name='EE'),
        'Extra Wide': Width(name='Extra Wide', short_name='4E')
    }
    product_type: str = 'shoes'
    color: str = None
    size: float = None
    length_of_insole: float = None
    width: Width = None

    ###############################################################################################
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


