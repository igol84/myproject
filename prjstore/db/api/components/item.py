import requests
from prjstore import schemas
from prjstore.db.api import settings
from prjstore.db import DB


class API_Item(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, new_item: schemas.item.CreateItem) -> schemas.item.ShowItemWithProduct:
        r = requests.post(f'{settings.host}/item', json=new_item.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.item.ShowItemWithProduct(**r.json())

    def update(self, new_item: schemas.item.UpdateItem) -> schemas.item.ShowItemWithProduct:
        r = requests.put(f"{settings.host}/item/{new_item.id}", json=new_item.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.item.ShowItemWithProduct(**r.json())

    def get_all(self) -> list[schemas.item.ShowItemWithProduct]:
        r = requests.get(f"{settings.host}/item", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return list(schemas.item.ListItems.parse_obj(r.json()))

    def get(self, item_id: int) -> schemas.item.ShowItemWithProduct:
        r = requests.get(f"{settings.host}/item/{item_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.item.ShowItemWithProduct(**r.json())

    def delete(self, item_id: int) -> bool:
        r = requests.delete(f"{settings.host}/item/{item_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
