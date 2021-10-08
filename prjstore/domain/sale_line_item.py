from pydantic.dataclasses import dataclass
from prjstore import schemas
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

    @staticmethod
    def create_from_schema(schema: schemas.sale_line_item.ShowSaleLineItemWithItem) -> 'SaleLineItem':
        item = Item.create_from_schema(schema.item)
        return SaleLineItem(item=item, sale_price=Money(schema.sale_price), qty=schema.qty)