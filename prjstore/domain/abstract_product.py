from dataclasses import field
from typing import Union, Optional

from abc import ABC

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from util.currency import Currency
from util.money import Money, Decimal, currencies


@dataclass
class AbstractProduct(ABC):
    prod_id: str
    name: str = field(default='item')
    price: Money = Money(0)

    ################################################################################################
    def convert_price(self, to_currency: str) -> None:
        self.price = Money.get_converted_money(self.price, to_currency)

    @validate_arguments
    def edit(self, name: Optional[str] = None, price: Union[None, Money, int, float, Decimal] = None,
             currency: Optional[str] = None) -> None:
        if name:
            self.name = str(name)
        if price:
            if isinstance(price, Money):
                self.price = price
            else:
                currency = currency if currency else self.price.currency
                if isinstance(currency, str):
                    currency = currencies[currency]
                self.price = Money(amount=float(price), currency=currency)
        elif currency:
            if isinstance(currency, str):
                currency = currencies[currency]
                self.price.currency = currency
            elif isinstance(currency, Currency):
                self.price.currency = currency

