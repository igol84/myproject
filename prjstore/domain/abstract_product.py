from typing import Union, Optional, Protocol

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from util.currency import Currency
from util.money import Money, Decimal


@dataclass
class AbstractProduct(Protocol):
    prod_id: str
    product_type: str
    name: str = 'item'
    price: Money = Money(0)

    ################################################################################################
    @validate_arguments
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
                    currency = Money.currencies[currency]
                self.price = Money(amount=float(price), currency=currency)
        elif currency:
            if isinstance(currency, str):
                currency = Money.currencies[currency]
                self.price.currency = currency
            elif isinstance(currency, Currency):
                self.price.currency = currency

    def schema_create(self, **kwargs) -> schemas.product.Product:
        return schemas.product.Product(id=self.prod_id, type=self.product_type, name=self.name, price=self.price.amount,
                                       **kwargs)
