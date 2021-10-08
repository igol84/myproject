import requests
from prjstore.schemas import sale_line_item as schemas
from prjstore.db.api import settings
from prjstore.db import DB


class API_SaleLineItem(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, new_sli: schemas.CreateSaleLineItem) -> schemas.ShowSaleLineItemWithItem:
        r = requests.post(f'{settings.host}/sale_line_item', json=new_sli.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.ShowSaleLineItemWithItem(**r.json())

    def update(self, new_sli: schemas.CreateSaleLineItem) -> schemas.ShowSaleLineItemWithItem:
        r = requests.put(f"{settings.host}/sale_line_item/{new_sli.sale_id}/{new_sli.item_id}/{new_sli.sale_price}",
                         json=new_sli.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.ShowSaleLineItemWithItem(**r.json())

    def get_all(self) -> list[schemas.ShowSaleLineItemWithItem]:
        r = requests.get(f"{settings.host}/sale_line_item", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return list(schemas.ListSaleLineItems.parse_obj(r.json()))

    def get(self, sale_id: int, item_id: int, sale_price: float) -> schemas.ShowSaleLineItemWithItem:
        r = requests.get(f"{settings.host}/sale_line_item/{sale_id}/{item_id}/{sale_price}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.ShowSaleLineItemWithItem(**r.json())

    def delete(self, sale_id: int, item_id: int, sale_price: float) -> bool:
        r = requests.delete(f"{settings.host}/sale_line_item/{sale_id}/{item_id}/{sale_price}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
