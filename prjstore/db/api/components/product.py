import requests
from prjstore import schemas
from prjstore.db.api import settings
from prjstore.db import DB


class API_Product(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, new_product: schemas.product.CreateProduct) -> schemas.product.Product:
        r = requests.post(f'{settings.host}/prod', data=new_product.json(), headers=self.headers)
        if r.status_code != 201:
            raise ConnectionError(r.status_code)
        else:
            return schemas.product.Product(**r.json())


    def update(self, product: schemas.product.Product) -> schemas.product.Product:
        r = requests.put(f"{settings.host}/prod/{product.id}", json=product.dict(), headers=self.headers)
        if r.status_code != 202:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.product.Product(**r.json())

    def get_all(self) -> list[schemas.product.Product]:
        r = requests.get(f"{settings.host}/prod", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return list(schemas.product.ListProducts.parse_obj(r.json()))

    def get(self, product_id: int) -> schemas.product.Product:
        r = requests.get(f"{settings.host}/prod/{product_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return schemas.product.Product(**r.json())

    def delete(self, product_id: int) -> bool:
        r = requests.delete(f"{settings.host}/prod/{product_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
