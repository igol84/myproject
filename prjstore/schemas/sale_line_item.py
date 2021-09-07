from pydantic import BaseModel
from prjstore.schemas.item import ShowItemWithProduct


class BaseSaleLineItem(BaseModel):
    qty: int


class CreateSaleLineItem(BaseSaleLineItem):
    sale_id: int
    item_id: int
    sale_price: float


class SaleLineItem(BaseSaleLineItem):
    sale_id: int
    item_id: int
    sale_price: float

    class Config:
        orm_mode = True


class ShowSaleLineItemWithItem(SaleLineItem):
    item: ShowItemWithProduct
