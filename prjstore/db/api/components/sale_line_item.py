from prjstore.db.api.components.base import APIBase
from prjstore.schemas import sale_line_item as schemas


class API_SaleLineItem(
    APIBase[schemas.CreateSaleLineItem, schemas.CreateSaleLineItem, schemas.ShowSaleLineItemWithItem]):
    prefix = 'sale_line_item'
    schema = schemas.ShowSaleLineItemWithItem
    list_schema = schemas.ListSaleLineItems
    keys = ['sale_id', 'item_id', 'sale_price']

    def __init__(self, headers):
        super().__init__(headers)
