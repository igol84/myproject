from pydantic import conint, validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_factory import ProductFactory
from util.money import Money


@dataclass
class Item:
    id: int
    product: AbstractProduct
    qty: conint(ge=0) = 1
    buy_price: Money = Money(0)

    @staticmethod
    def create_from_schema(schema: schemas.item.ShowItemWithProduct) -> 'Item':
        product = ProductFactory.create_from_schema(schema.product)
        return Item(id=schema.id, product=product, qty=schema.qty, buy_price=Money(schema.buy_price))

    @validate_arguments
    def schema_create(self, store_id: int) -> schemas.item.ShowItemWithProduct:
        product = self.product.schema_create()
        return schemas.item.ShowItemWithProduct(id=self.id, prod_id=self.product.prod_id, store_id=store_id,
                                                qty=self.qty, buy_price=self.buy_price.amount, product=product)
