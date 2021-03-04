from contracts import contract, new_contract
from abc import ABCMeta
from util.money_my import MoneyMy


class ProductDesc(metaclass=ABCMeta):
    """
>>> pr = ProductDesc(item_id='2', desc='item2', price=700)# Create product
>>> pr                                                    # Get product
<Product: id=2, desc=item2, price=UAH 700.00>
>>> pr.id                                                 # Get id
'2'
>>> pr.desc = 'new item'                                  # Change desc
>>> print(pr.desc)                                        # Get desc
new item
>>> pr.price = 750.50                                     # Change price
>>> print(pr.price)                                       # Get price
UAH 750.50
>>> pr.convert_price('USD')                                    # Convert Price
>>> print(pr.price)
USD 27.29
>>> pr.edit(desc='item3', price=500, currency='USD')      # Edit product
>>> pr
<Product: id=2, desc=item3, price=USD 500.00>
>>> pr.edit(desc='item2')                                 # Edit name
>>> pr
<Product: id=2, desc=item2, price=USD 500.00>
>>> pr.edit(price=300)                                    # Edit desc
>>> pr
<Product: id=2, desc=item2, price=USD 300.00>
>>> pr.edit(currency='UAH')                               # Edit currency
>>> shoes = Shoes(item_id='6', desc='nike air force', price=900, size=44)# Create product
>>> shoes                                                    # Get product
<Shoes: id=6, desc=nike air force, price=UAH 900.00, size=44.0>
>>> shoes.size                                                 # Get id
44.0
>>> pr.size = '43.2'                                     # Change price
>>> print(pr.size)
43.2
    """
    _default_curr = MoneyMy.default_currency

    @contract
    def __init__(self, item_id: 'str', desc: 'str' = 'item', price=0, currency: 'str' = _default_curr):
        self._item_id = item_id
        self._desc = desc
        self._price = MoneyMy(amount=str(price), currency=currency)

    def __repr__(self) -> str:
        return f'<Product: id={self._item_id}, desc={self._desc}, price={self._price}>'

    def get_id(self) -> str:
        return self._item_id

    id = property(get_id)

    def get_price(self) -> MoneyMy:
        return self._price

    def set_price(self, price, currency=None) -> None:
        curr = currency if currency else self._price.currency
        self._price = MoneyMy(amount=str(price), currency=curr)

    price = property(get_price, set_price)

    def convert_price(self, to_currency) -> None:
        self._price = MoneyMy.get_converted_money(self._price, to_currency)

    def get_desc(self) -> str:
        return self._desc

    @contract
    def set_desc(self, desc: 'str') -> None:
        self._desc = desc

    desc = property(get_desc, set_desc)

    def edit(self, desc=None, price=None, currency=None) -> None:
        if desc:
            self.set_desc(desc)
        if price:
            self.set_price(price, currency)
        elif currency:
            self.set_price(self._price.amount, currency)


class Shoes(ProductDesc):
    _default_curr = MoneyMy.default_currency

    new_contract('valid_size', lambda size: float(size) and 0 < float(size) < 60)

    @contract
    def __init__(self, item_id: 'str', desc: 'str' = 'item', price=0, size: 'valid_size, *' = 40,
                 currency: 'str' = _default_curr):
        super().__init__(item_id, desc, price, currency)
        self._size = float(size)

    def get_size(self) -> float:
        return self._size


    @contract
    def set_size(self, size: 'valid_size, *') -> None:
        self._size = float(size)

    size = property(get_size, set_size)

    def __repr__(self) -> str:
        return f'<Shoes: id={self._item_id}, desc={self._desc}, price={self._price}, size={self._size}>'
