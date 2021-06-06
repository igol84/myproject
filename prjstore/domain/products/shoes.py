import dataclasses
from decimal import Decimal
from typing import Union, Optional

from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes_components import Width
from util.money import Money


widths: dict[str, Width] = {
        'Medium': Width(name='Medium', short_name='D'),
        'Wide': Width(name='Wide', short_name='EE'),
        'Extra Wide': Width(name='Extra Wide', short_name='4E')
    }
@dataclass
class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(prod_id='6', name='nike air force', price=Money(900), color='red', \
size=43, width=widths['Wide'], length_of_insole=28.5) # Create product
>>> d = dataclasses.astuple(shoes)
>>> d
('6', 'nike air force', (900.0, ('UAH', 27.5, '₴')), 'red', 43.0, 28.5, ('Wide', 'EE'))
>>> shoes2 = Shoes(*d)
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


>>> shoes.width = widths['Medium']
>>> shoes.width.name
'Medium'
>>> shoes.width.short_name
'D'

>>> shoes.edit(name='nike air', price=500, color='red', size='42', \
width='Wide', length_of_insole=28.5)      # Edit product
>>> shoes
Shoes(prod_id='6', name='nike air', price=Money(amount=500.0, currency=Currency(code='UAH', rate=27.5, sign='₴')), \
color='red', size=42.0, length_of_insole=28.5, width=Width(name='Wide', short_name='EE'))
    """
    color: str = None
    size: float = None
    length_of_insole: float = None
    width: Width = None

    ###############################################################################################

    def edit(self,
             name: Optional[str] = None,
             price: Union[None, Money, int, float, Decimal] = None,
             currency: Optional[str] = None,
             color: Optional[str] = None,
             size: Union[int, float] = None,
             length_of_insole: Union[None, int, float] = None,
             width: Union[None, Width, str] = None
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
            elif isinstance(width, str) and width in widths:
                self.width = widths[width]
            else:
                raise ValueError('Dont find width: ', width)


