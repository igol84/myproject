from pydantic.dataclasses import dataclass

from util.money import Money
from prjstore.domain.item import Item


@dataclass
class SaleLineItem:
    item: Item
    sale_price: Money = None
    qty: int = 1

    def __post_init__(self):
        if self.sale_price is None:
            self.sale_price: Money = self.item.product.price
