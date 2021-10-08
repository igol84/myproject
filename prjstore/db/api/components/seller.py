import requests
from prjstore import schemas
from prjstore.db.api import settings
from prjstore.db import DB


class API_Seller(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, new_seller: schemas.seller.CreateSeller) -> schemas.seller.Seller:
        r = requests.post(f'{settings.host}/seller', json=new_seller.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.seller.Seller(**r.json())

    def update(self, seller: schemas.seller.UpdateSeller) -> schemas.seller.Seller:
        r = requests.put(f"{settings.host}/seller/{seller.id}", json=seller.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.seller.Seller(**r.json())

    def get_all(self) -> list[schemas.seller.Seller]:
        r = requests.get(f"{settings.host}/seller", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return list(schemas.seller.ListSeller.parse_obj(r.json()))

    def get(self, seller_id: int) -> schemas.seller.Seller:
        r = requests.get(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.seller.Seller(**r.json())

    def delete(self, seller_id: int) -> bool:
        r = requests.delete(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
