from pydantic import BaseModel

from prjstore.db.schemas.item import CreateItem, UpdateItem
from prjstore.db.schemas.sale import CreateSale, ShowSaleWithSLIs
from prjstore.db.schemas.sale_line_item import SaleLineItem


class EndSale(BaseModel):
    sale: CreateSale


class OutputEndSale(BaseModel):
    sale: ShowSaleWithSLIs


class EditSLIPrice(BaseModel):
    old_sli: SaleLineItem
    new_sli: SaleLineItem


class SaleLineItemKeys(BaseModel):
    sale_id: int
    item_id: int
    sale_price: float


class PutItemFromOldSale(BaseModel):
    sale_id: int
    list_del_sli: list[SaleLineItemKeys]
    list_new_items: list[CreateItem]
    list_update_items: list[UpdateItem]
    delete: bool = False
