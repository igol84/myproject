"""
    >>> pr = ProductDesc(item_id=2, desc='item2', price=700)  # Create product
    >>> pr                                                    # Get product
    <Product: id=2, desc=item2, price=UAH 700.00>
    >>> pr.id                                                 # Get id
    2
    >>> pr.desc = 'new item'                                  # Change desc
    >>> print(pr.desc)                                        # Get desc
    new item
    >>> pr.price = 750.50                                     # Change price
    >>> print(pr.price)                                       # Get price
    UAH 750.50
    >>> pr.convert_price()                                    # Convert Price
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
    >>> pr
    <Product: id=2, desc=item2, price=UAH 300.00>


    >>> pr2 = ProductDesc(desc='item3', price=800, currency='USD')  # Create new product with new generated id
    >>> pr2
    <Product: id=3, desc=item3, price=USD 800.00>


"""
from contracts import contract
from abc import ABCMeta
from util.money_my import MoneyMy, get_converted_Money


class ProductDesc(metaclass=ABCMeta):
    __lid = 1  # counter of id product
    _default_curr = MoneyMy.default_currency

    @contract
    def __init__(self, item_id=None, desc: 'str' = 'item', price=0, currency=_default_curr):
        self._item_id = item_id if item_id else ProductDesc.__lid
        self._desc = desc
        self._price = MoneyMy(amount=str(price), currency=currency)
        ProductDesc.__lid = self._item_id + 1

    def __repr__(self):
        return f'<Product: id={self._item_id}, desc={self._desc}, price={self._price}>'

    def get_id(self):
        return self._item_id

    id = property(get_id)

    def get_price(self):
        return self._price

    def set_price(self, price, currency=None):
        curr = currency if currency else self._price.currency
        self._price = MoneyMy(amount=str(price), currency=curr)

    price = property(get_price, set_price)

    def convert_price(self):
        self._price = get_converted_Money(self._price)

    def get_desc(self):
        return self._desc

    @contract
    def set_desc(self, desc: 'str'):
        self._desc = desc

    desc = property(get_desc, set_desc)

    def edit(self, desc=None, price=None, currency=None):
        if desc:
            self.set_desc(desc)
        if price:
            self.set_price(price, currency)
        elif currency:
            self.set_price(self._price.amount, currency)
