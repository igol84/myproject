from contracts import contract
from abc import ABCMeta
from util.money_my import MoneyMy


class AbstractProduct(metaclass=ABCMeta):
    """
    """
    _default_curr = MoneyMy.default_currency

    @contract(item_id='str', desc='str', currency='str')
    def __init__(self, item_id, desc='item', price=0, currency=_default_curr):
        self._item_id = item_id
        self._desc = desc
        self._price = MoneyMy(amount=str(price), currency=currency)

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

    @contract(desc='str')
    def set_desc(self, desc) -> None:
        self._desc = desc

    desc = property(get_desc, set_desc)

    def edit(self, desc=None, price=None, currency=None) -> None:
        if desc:
            self.set_desc(desc)
        if price:
            self.set_price(price, currency)
        elif currency:
            self.set_price(self._price.amount, currency)

    def __repr__(self) -> str:
        pass
