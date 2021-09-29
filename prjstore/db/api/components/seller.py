import requests
from prjstore import schemas
from prjstore.domain.seller import Seller
from prjstore.db.api import settings
from prjstore.db import DB


class API_Seller(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, store_id: int, name: str) -> Seller:
        new_seller = schemas.seller.CreateSeller(store_id=store_id, name=name)
        r = requests.post(f'{settings.host}/seller', json=new_seller.dict(), headers=self.headers)
        if r.status_code != 201:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller_pd = schemas.seller.Seller(**r.json())
            return Seller(id=seller_pd.id, name=seller_pd.name)

    def update(self, seller_id: int, store_id: int, name: str) -> Seller:
        new_seller = schemas.seller.CreateSeller(store_id=store_id, name=name)
        r = requests.put(f"{settings.host}/seller/{seller_id}", json=new_seller.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller_pd = schemas.seller.Seller(**r.json())
            return Seller(id=seller_pd.id, name=seller_pd.name)

    def get_all(self) -> dict[int, Seller]:
        r = requests.get(f"{settings.host}/seller", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sellers_pd: list[schemas.seller.Seller] = schemas.seller.ListSeller.parse_obj(r.json())
            return {seller_pd.id: Seller(id=seller_pd.id, name=seller_pd.name) for seller_pd in sellers_pd}

    def get(self, seller_id: int) -> Seller:
        r = requests.get(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller_pd = schemas.seller.Seller(**r.json())
            return Seller(id=seller_id, name=seller_pd.name)

    def delete(self, seller_id: int) -> bool:
        r = requests.delete(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
