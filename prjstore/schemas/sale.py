from pydantic import BaseModel
from datetime import datetime
from prjstore.schemas.sale_line_item import ShowSaleLineItemWithItem, CreateSaleLineItemForSale
from prjstore.schemas.seller import Seller
from prjstore.schemas.place import Place


class BaseSale(BaseModel):
    place_id: int
    seller_id: int
    date_time: datetime


class CreateSale(BaseSale):
    sale_line_items: list[CreateSaleLineItemForSale]


class UpdateSale(BaseSale):
    id: int
    sale_line_items: list[CreateSaleLineItemForSale]


class Sale(BaseSale):
    id: int

    class Config:
        orm_mode = True


class ShowSaleWithSLIs(Sale):
    sale_line_items: list[ShowSaleLineItemWithItem]
    seller: Seller
    place: Place


class ListSale(BaseModel):
    __root__: list[ShowSaleWithSLIs]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
