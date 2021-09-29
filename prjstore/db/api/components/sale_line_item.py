import requests
from prjstore import schemas
from prjstore.db.api.components.item import API_Item
from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.db.api import settings
from prjstore.db import DB
from util.money import Money


class API_SaleLineItem(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, sale_id: int, item_id: int, sale_price: float, qty: int) -> SaleLineItem:
        new_sale_line_item = schemas.sale_line_item.CreateSaleLineItem(
            qty=qty, sale_id=sale_id, item_id=item_id, sale_price=sale_price
        )
        r = requests.post(f'{settings.host}/sale_line_item', json=new_sale_line_item.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sale_line_item_pd = schemas.sale_line_item.SaleLineItem(**r.json())
            item = API_Item(self.headers).get(sale_line_item_pd.item_id)
            return SaleLineItem(item=item, sale_price=Money(sale_line_item_pd.sale_price), qty=sale_line_item_pd.qty)

    def update(self, sale_id: int, item_id: int, sale_price: float, qty: int) -> SaleLineItem:
        new_sale_line_item = schemas.sale_line_item.CreateSaleLineItem(
            sale_id=sale_id, item_id=item_id, sale_price=sale_price, qty=qty
        )
        r = requests.put(f"{settings.host}/sale_line_item/{sale_id}/{item_id}/{sale_price}",
                         json=new_sale_line_item.dict(),
                         headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sale_line_item_pd = schemas.sale_line_item.SaleLineItem(**r.json())
            item = API_Item(self.headers).get(sale_line_item_pd.item_id)
            return SaleLineItem(item=item, sale_price=Money(sale_line_item_pd.sale_price), qty=sale_line_item_pd.qty)

    def get_all(self) -> list[SaleLineItem]:
        r = requests.get(f"{settings.host}/sale_line_item", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sale_line_items_pd: list[schemas.sale_line_item.SaleLineItem]
            sale_line_items_pd = schemas.sale_line_item.ListSaleLineItems.parse_obj(r.json())
            sale_line_items: list[SaleLineItem] = []
            for sale_line_item_pd in sale_line_items_pd:
                item = API_Item(self.headers).get(sale_line_item_pd.item_id)
                sale_line_items.append(
                    SaleLineItem(item=item, sale_price=Money(sale_line_item_pd.sale_price), qty=sale_line_item_pd.qty)
                )
            return sale_line_items

    def get(self, sale_id: int, item_id: int, sale_price: float) -> SaleLineItem:
        r = requests.get(f"{settings.host}/sale_line_item/{sale_id}/{item_id}/{sale_price}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sale_line_item_pd = schemas.sale_line_item.SaleLineItem(**r.json())
            item = API_Item(self.headers).get(sale_line_item_pd.item_id)
            return SaleLineItem(item=item, sale_price=Money(sale_line_item_pd.sale_price), qty=sale_line_item_pd.qty)

    def delete(self, sale_id: int, item_id: int, sale_price: float) -> bool:
        r = requests.delete(f"{settings.host}/sale_line_item/{sale_id}/{item_id}/{sale_price}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
