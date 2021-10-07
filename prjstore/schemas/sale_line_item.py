from pydantic import BaseModel
from prjstore.schemas.item import ShowItemWithProduct


class BaseSaleLineItem(BaseModel):
    qty: int


class CreateSaleLineItem(BaseSaleLineItem):
    sale_id: int
    item_id: int
    sale_price: float


class CreateSaleLineItemForSale(BaseSaleLineItem):
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


class ListSaleLineItems(BaseModel):
    __root__: list[SaleLineItem]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
