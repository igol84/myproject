from contracts import contract, new_contract
from prjstore.domain.abstract_product import AbstractProduct


class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(id='6', name='nike air force', price=900, size=43, width='Wide')# Create product
>>> shoes                                                    # Get product
<Shoes: id=6, name=nike air force, price=UAH 900.00, size=43.0, width=Wide>
>>> shoes.size=44                                                 # Get size
>>> shoes.size
44.0

>>> shoes.width='Medium'                                                 # Get width
>>> shoes.width
'Medium'

>>> shoes.edit(name='nike air', price=500, size='42', width='Wide', currency='USD')      # Edit product
>>> shoes
<Shoes: id=6, name=nike air, price=USD 500.00, size=42.0, width=Wide>
    """

    @staticmethod
    @new_contract
    def valid_size(size):
        return float(size) and 0 < float(size) < 60

    @contract(id=str, name=str, price='int | float', size='valid_size', currency=str)
    def __init__(self, id, name='item', price=0, size=1, width='Medium', currency=AbstractProduct._default_curr):
        super().__init__(id, name, price, currency)
        self.size = size
        self.width = width

    def get_size(self) -> float:
        return self._size

    @contract(size='valid_size')
    def set_size(self, size) -> None:
        self._size = float(size)

    size = property(get_size, set_size)

    def get_width(self) -> str:
        return self._width

    @contract(width=str)
    def set_width(self, width) -> None:
        self._width = str(width)

    width = property(get_width, set_width)

    def edit(self, name=None, price=None, currency=None, size=None, width=None) -> None:
        AbstractProduct.edit(self, name, price, currency)
        if size:
            self.set_size(size)
        if width:
            self.set_width(width)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}, name={self.name}, price={self.price}, size={self.size}, ' \
               f'width={self.width}>'
