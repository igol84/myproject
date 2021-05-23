from typing import Union, Optional

from contracts import contract
from abc import ABC, abstractmethod
from util.money_my import MoneyMy, Decimal


class AbstractProduct(ABC):
    """
    """
    _default_curr = MoneyMy.default_currency

    @contract(product_id='str | int')
    def __init__(self, product_id: Union[str, int], name: str = 'item', price=0, currency=_default_curr):
        self.__id: str = str(product_id)
        self.name: str = name
        self.__price: MoneyMy = None
        self.__set_price(price, currency)

    ###############################################################################################
    # id
    def __get_id(self) -> str:
        return self.__id

    id: str = property(__get_id)

    ###############################################################################################
    # name
    def __get_name(self) -> str:
        return self.__name

    @contract(name='str')
    def __set_name(self, name: str) -> None:
        self.__name = name

    name: str = property(__get_name, __set_name)

    ###############################################################################################
    # price
    def __get_price(self) -> MoneyMy:
        return self.__price

    @contract(price='$MoneyMy | int | float | $Decimal', currency='None | str')
    def __set_price(self,
                  price: Union[MoneyMy, int, float, Decimal],
                  currency: Optional[str] = None
                  ) -> None:
        if isinstance(price, MoneyMy):
            self.__price = price
        else:
            curr = currency if currency else self.__price.currency
            self.__price = MoneyMy(amount=str(price), currency=curr)

    price: MoneyMy = property(__get_price, __set_price)

    ################################################################################################
    def convert_price(self, to_currency: str) -> None:
        self.__price = MoneyMy.get_converted_money(self.__price, to_currency)

    def edit(self,
             name: Optional[str] = None,
             price: Union[None, MoneyMy, int, float, Decimal] = None,
             currency: Optional[str] = None
             ) -> None:
        if name:
            self.__set_name(name)
        if price:
            self.__set_price(price, currency)
        elif currency:
            self.__set_price(self.price.amount, currency)

    @abstractmethod
    def __repr__(self) -> str:
        pass
