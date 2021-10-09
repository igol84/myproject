from prjstore.db.api.components.base import APIBase
from prjstore.schemas import sale_line_item as sch


class API_SaleLineItem(
    APIBase[sch.CreateSaleLineItem, sch.CreateSaleLineItem, sch.ShowSaleLineItemWithItem]):
    prefix = 'sale_line_item'
    schema = sch.ShowSaleLineItemWithItem
    list_schema = sch.ListSaleLineItems
    keys = ['sale_id', 'item_id', 'sale_price']

    def __init__(self, headers):
        super().__init__(headers)
