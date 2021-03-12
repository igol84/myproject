from contracts import contract, new_contract
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.products.shoes_components import Width

class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(prod_id='6', name='nike air force', price=900, color='red', \
size=43, width=Width(name='Wide', short_name='EE'), length_of_insole=28.5) # Create product
>>> shoes
<Shoes: id=6, name=nike air force, price=UAH 900.00, color=red, size=43.0, length_of_insole=28.5, width=Wide>
>>> shoes.color='black'
>>> shoes.color
'black'

>>> shoes.size=44                                                 # Get size
>>> shoes.size
44.0

>>> shoes.length_of_insole=28
>>> shoes.length_of_insole
28.0


>>> shoes.width = Width(name='Medium', short_name='D')                                                 # Get width
>>> shoes.width
Medium
>>> shoes.width.short_name
'D'

>>> shoes.edit(name='nike air', price=500, color='red', size='42', \
width=Width(name='Wide', short_name='EE'), length_of_insole=28.5, currency='USD')      # Edit product
>>> shoes
<Shoes: id=6, name=nike air, price=USD 500.00, color=red, size=42.0, length_of_insole=28.5, width=Wide>
    """

    @staticmethod
    @new_contract
    def valid_size(size):
        return float(size) and 0 < float(size) < 60

    @staticmethod
    @new_contract
    def valid_length_of_insole(length_of_insole):
        return float(length_of_insole) and 10 < float(length_of_insole) < 40

    @contract(prod_id=str, name=str, price='int | float', size='valid_size', currency=str)
    def __init__(self, prod_id, name='item', price=0, color='default', size=1, length_of_insole=11,
                 width=Width(name='Medium', short_name='D'),
                 currency=AbstractProduct._default_curr):
        super().__init__(prod_id, name, price, currency)
        self.color = color
        self.size = size
        self.length_of_insole = length_of_insole
        self.width = width

    def get_color(self) -> str:
        return self._color

    @contract(color=str)
    def set_color(self, color) -> None:
        self._color = color

    color = property(get_color, set_color)

    def get_size(self) -> float:
        return self._size

    @contract(size='valid_size')
    def set_size(self, size) -> None:
        self._size = float(size)

    size = property(get_size, set_size)

    def get_length_of_insole(self) -> float:
        return self._length_of_insole

    @contract(length_of_insole='valid_length_of_insole')
    def set_length_of_insole(self, length_of_insole) -> None:
        self._length_of_insole = float(length_of_insole)

    length_of_insole = property(get_length_of_insole, set_length_of_insole)

    def get_width(self) -> Width:
        return self._width

    @contract(width=Width)
    def set_width(self, width) -> None:
        self._width = width

    width = property(get_width, set_width)

    def edit(self, name=None, price=None, currency=None, color=None, size=None,
             length_of_insole=None, width=None) -> None:
        AbstractProduct.edit(self, name, price, currency)
        if color:
            self.set_color(color)
        if size:
            self.set_size(size)
        if length_of_insole:
            self.set_length_of_insole(length_of_insole)
        if width:
            self.set_width(width)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}, name={self.name}, price={self.price}, color={self.color}, ' \
               f'size={self.size}, length_of_insole={self.length_of_insole}, width={self.width}>'
