from typing import Union, Optional

from contracts import contract
from abc import ABC, abstractmethod
from util.money_my import MoneyMy, Decimal


class AbstractProduct(ABC):
    """
    """
    _default_curr = MoneyMy.default_currency

    @contract(id='str | int')
    def __init__(self, id: Union[str, int], name: str = 'item', price=0, currency=_default_curr):
        self._id = str(id)
        self.name = name
        self.set_price(price, currency)

    ################################################################################################ id
    def get_id(self) -> str:
        return self._id

    id = property(get_id)

    def get_name(self) -> str:
        return self._name

    ################################################################################################ name
    @contract(name='str')
    def set_name(self, name: str) -> None:
        self._name = name

    name = property(get_name, set_name)

    ################################################################################################ price
    def get_price(self) -> MoneyMy:
        return self._price

    @contract(price='$MoneyMy | int | float | $Decimal', currency='None | str')
    def set_price(self,
                  price: Union[MoneyMy, int, float, Decimal],
                  currency: Optional[str] = None
                  ) -> None:
        if isinstance(price, MoneyMy):
            self._price = price
        else:
            curr = currency if currency else self._price.currency
            self._price = MoneyMy(amount=str(price), currency=curr)

    price = property(get_price, set_price)

    ################################################################################################
    def convert_price(self, to_currency) -> None:
        self._price = MoneyMy.get_converted_money(self._price, to_currency)

    def edit(self, name=None, price=None, currency=None) -> None:
        if name:
            self.set_name(name)
        if price:
            self.set_price(price, currency)
        elif currency:
            self.set_price(self.price.amount, currency)

    @abstractmethod
    def __repr__(self) -> str:
        pass
