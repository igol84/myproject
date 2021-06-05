from decimal import Decimal
from typing import Union, Optional

from contracts import contract, new_contract
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes_components import Width
from util.money import Money


class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(prod_id='6', name='nike air force', price=900, color='red', \
size=43, width=Shoes.widths['Wide'], length_of_insole=28.5) # Create product
>>> shoes
<Shoes: id=6, name=nike air force, price=UAH 900.00, color=red, size=43.0, length_of_insole=28.5, width=Wide>
>>> shoes.color='black'
>>> shoes.color
'black'

>>> shoes.size=44
>>> shoes.size
44.0

>>> shoes.length_of_insole=28
>>> shoes.length_of_insole
28.0


>>> shoes.width = Shoes.widths['Medium']
>>> shoes.width
Medium
>>> shoes.width.short_name
'D'

>>> shoes.width = 'Extra Wide'
>>> shoes.width
Extra Wide
>>> shoes.width.short_name
'4E'

>>> shoes.edit(name='nike air', price=500, color='red', size='42', \
width=Width(name='Wide', short_name='EE'), length_of_insole=28.5, currency='USD')      # Edit product
>>> shoes
<Shoes: id=6, name=nike air, price=USD 500.00, color=red, size=42.0, length_of_insole=28.5, width=Wide>
    """
    widths: dict[str, Width] = {
        'Medium': Width(name='Medium', short_name='D'),
        'Wide': Width(name='Wide', short_name='EE'),
        'Extra Wide': Width(name='Extra Wide', short_name='4E')
    }

    @staticmethod
    @new_contract
    def valid_size(size) -> float:
        return float(size) and 0 < float(size) < 60

    @staticmethod
    @new_contract
    def valid_length_of_insole(length_of_insole) -> float:
        return float(length_of_insole) and 9 < float(length_of_insole) < 40

    @contract(price='int | float', color=str, size='valid_size',
              length_of_insole='valid_length_of_insole', currency=str)
    def __init__(self,
                 prod_id: str,
                 name: str = 'item',
                 price: Union[Money, int, float, Decimal] = 0,
                 color: str = 'default',
                 size: Union[int, float] = 1,
                 length_of_insole: Union[int, float] = 11,
                 width: Union[Width, str] = widths['Medium'],
                 currency: str = AbstractProduct._default_curr):
        super().__init__(prod_id, name, price, currency)
        self.color: str = color
        self.size: float = size
        self.length_of_insole: float = length_of_insole
        self.width: Width = width

    ###############################################################################################
    # color
    def __get_color(self) -> str:
        return self.__color

    @contract(color=str)
    def __set_color(self, color) -> None:
        self.__color = color

    color = property(__get_color, __set_color)

    ###############################################################################################
    # size
    def __get_size(self) -> float:
        return self.__size

    @contract(size='valid_size')
    def __set_size(self, size) -> None:
        self.__size = float(size)

    size = property(__get_size, __set_size)

    ###############################################################################################
    # length_of_insole
    def __get_length_of_insole(self) -> float:
        return self.__length_of_insole

    @contract(length_of_insole='valid_length_of_insole')
    def __set_length_of_insole(self, length_of_insole) -> None:
        self.__length_of_insole = float(length_of_insole)

    length_of_insole = property(__get_length_of_insole, __set_length_of_insole)

    ###############################################################################################
    # width
    def __get_width(self) -> Width:
        return self.__width

    @contract(width='$Width | str')
    def __set_width(self, width: Union[Width, str]) -> None:
        if isinstance(width, Width):
            self.__width = width
        else:
            if width in Shoes.widths:
                self.__width = Shoes.widths[width]
            else:
                raise IndexError(f"Invalid value width: {width}")

    width = property(__get_width, __set_width)

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
            self.__set_color(color)
        if size:
            self.__set_size(size)
        if length_of_insole:
            self.__set_length_of_insole(length_of_insole)
        if width:
            self.__set_width(width)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}, name={self.name}, price={self.price}, color={self.color}, ' \
               f'size={self.size}, length_of_insole={self.length_of_insole}, width={self.width}>'
