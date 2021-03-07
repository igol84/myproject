from contracts import contract, new_contract
from prjstore.domain.abstract_product import AbstractProduct


class Shoes(AbstractProduct):
    """
>>> shoes = Shoes(item_id='6', desc='nike air force', price=900, size=44)# Create product
>>> shoes                                                    # Get product
<Shoes: id=6, desc=nike air force, price=UAH 900.00, size=44.0>
>>> shoes.size                                                 # Get id
44.0
    """

    new_contract('valid_size', lambda size: float(size) and 0 < float(size) < 60)

    @contract
    def __init__(self, item_id: 'str', desc: 'str' = 'item', price=0, size: 'valid_size, *' = 40,
                 currency: 'str' = AbstractProduct._default_curr):
        super().__init__(item_id, desc, price, currency)
        self._size = float(size)

    def get_size(self) -> float:
        return self._size

    @contract
    def set_size(self, size: 'valid_size, *') -> None:
        self._size = float(size)

    size = property(get_size, set_size)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self._item_id}, desc={self._desc}, price={self._price}, size={self._size}>'
