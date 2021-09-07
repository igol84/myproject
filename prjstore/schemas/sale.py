from pydantic import BaseModel
from datetime import datetime
from prjstore.schemas.sale_line_item import ShowSaleLineItemWithItem
from prjstore.schemas.seller import Seller
from prjstore.schemas.place import Place


class BaseSale(BaseModel):
    store_id: int
    seller_id: int
    place_id: int
    date_time: datetime


class CreateSale(BaseSale):
    pass


class Sale(BaseSale):
    id: int

    class Config:
        orm_mode = True


class ShowSaleWithSLIs(Sale):
    sale_line_items: list[ShowSaleLineItemWithItem]
    seller: Seller
    place: Place
