import requests

from prjstore.db import DB
from prjstore import schemas
from prjstore.domain.seller import Seller

from prjstore.db.api import settings
from prjstore.db.api.authorization import auth


class API_DB(DB):
    headers = auth()

    def create_seller(self, store_id:int, name:str) ->  dict[int: Seller]:
        new_seller = schemas.seller.CreateSeller(store_id=store_id, name=name)
        r = requests.post(f'{settings.host}/seller', json=new_seller.dict(), headers=self.headers)
        if (r.status_code != 201):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller = schemas.seller.Seller(**r.json())
            return {seller.id: Seller(name=seller.name)}

    def update_seller(self, seller_id: int, store_id:int, name:str) -> dict[int: Seller]:
        new_seller = schemas.seller.CreateSeller(store_id=store_id, name=name)
        r = requests.put(f"{settings.host}/seller/{seller_id}", json=new_seller.dict(), headers=self.headers)
        if (r.status_code != 202):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller = schemas.seller.Seller(**r.json())
            return {seller.id: Seller(name=seller.name)}


    def get_all_sellers(self) -> dict[int: Seller]:
        r = requests.get(f"{settings.host}/seller", headers=self.headers)
        if (r.status_code != 200):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            sellers: list[schemas.seller.Seller] = schemas.seller.ListSeller.parse_obj(r.json())
            return {seller.id: Seller(name=seller.name) for seller in sellers}

    def get_seller(self, seller_id: int) -> Seller:
        r = requests.get(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if (r.status_code != 200):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller = schemas.seller.Seller(**r.json())
            return Seller(name=seller.name)

    def delete_seller(self, seller_id: int) -> bool:
        r = requests.delete(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if (r.status_code != 204):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True


if __name__ == '__main__':
    db = API_DB()
    seller = db.get_seller(seller_id=2)
    print(seller)
    sellers = db.get_all_sellers()
    print(sellers)
    print(len(sellers))
    print(list(sellers.values())[0])
