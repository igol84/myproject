from datetime import date

from pydantic import conint, validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory
from util.money import Money


@dataclass
class Item:
    product: AbstractProduct
    id: int = None
    qty: conint(ge=0) = 1
    buy_price: Money = Money(0)
    date_buy: date = date.today()

    @staticmethod
    def create_from_schema(schema: schemas.item.ShowItemWithProduct, pc: ProductCatalog = None) -> 'Item':
        product = ProductFactory.create_from_schema(schema.product)
        if pc and schema.product.id in pc.products:
            product = pc[schema.product.id]
        return Item(id=schema.id, product=product, qty=schema.qty, buy_price=Money(schema.buy_price),
                    date_buy=schema.date_buy)

    @staticmethod
    def create_from_schema_with_product(schema: schemas.item.Item, product: AbstractProduct) -> 'Item':
        return Item(id=schema.id, product=product, qty=schema.qty, buy_price=Money(schema.buy_price),
                    date_buy=schema.date_buy)

    @validate_arguments
    def schema_create(self, store_id: int) -> schemas.item.ShowItemWithProduct:
        product = self.product.schema_create()
        return schemas.item.ShowItemWithProduct(
            id=self.id, prod_id=self.product.prod_id, store_id=store_id, qty=self.qty, buy_price=self.buy_price.amount,
            product=product, date_buy=self.date_buy)
