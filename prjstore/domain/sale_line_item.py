from pydantic.dataclasses import dataclass

from prjstore.domain.product_catalog import get_products_for_test
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

def get_items_for_test() -> list[Item]:
    test_pc = get_products_for_test()
    items= [Item(product=test_pc.products['2'], qty=3),
             Item(product=test_pc.products['4'], qty=1),
             Item(product=test_pc.products['6'], qty=2)]
    return items