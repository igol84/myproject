import requests
from prjstore import schemas
from prjstore.db.api.components.product import API_Product
from prjstore.domain.item import Item
from prjstore.db.api import settings
from prjstore.db import DB
from util.money import Money


class API_Item(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, prod_id: int, store_id: int, qty: int, buy_price: float) -> Item:
        new_item = schemas.item.CreateItem(prod_id=prod_id, store_id=store_id, qty=qty, buy_price=buy_price)
        r = requests.post(f'{settings.host}/item', json=new_item.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            item_pd = schemas.item.Item(**r.json())
            product = API_Product(self.headers).get(item_pd.prod_id)
            return Item(id=item_pd.id, product=product, qty=item_pd.qty, buy_price=Money(item_pd.buy_price))

    def update(self, item_id: int, prod_id: int, store_id: int, qty: int, buy_price: float) -> Item:
        new_item = schemas.item.CreateItem(prod_id=prod_id, store_id=store_id, qty=qty, buy_price=buy_price)
        r = requests.put(f"{settings.host}/item/{item_id}", json=new_item.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            item_pd = schemas.item.Item(**r.json())
            product = API_Product(self.headers).get(item_pd.prod_id)
            return Item(id=item_pd.id, product=product, qty=item_pd.qty, buy_price=Money(item_pd.buy_price))

    def get_all(self) -> dict[int, Item]:
        r = requests.get(f"{settings.host}/item", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            items_pd: list[schemas.item.Item] = schemas.item.ListItems.parse_obj(r.json())
            items: dict[int, Item] = {}
            for item_pd in items_pd:
                product = API_Product(self.headers).get(item_pd.prod_id)
                items[item_pd.id] = Item(id=item_pd.id, product=product, qty=item_pd.qty,
                                         buy_price=Money(item_pd.buy_price))
            return items

    def get(self, item_id: int) -> Item:
        r = requests.get(f"{settings.host}/item/{item_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            item_pd = schemas.item.Item(**r.json())
            product = API_Product(self.headers).get(item_pd.prod_id)
            return Item(id=item_pd.id, product=product, qty=item_pd.qty, buy_price=Money(item_pd.buy_price))

    def delete(self, item_id: int) -> bool:
        r = requests.delete(f"{settings.host}/item/{item_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
