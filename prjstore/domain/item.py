from pydantic import conint
from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from util.money import Money


@dataclass
class Item:
    product: AbstractProduct
    qty: conint(ge=0) = 1
    buy_price: Money = Money(0)
