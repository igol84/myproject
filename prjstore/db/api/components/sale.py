import requests
from datetime import datetime
from prjstore import schemas
from prjstore.db.api import settings
from prjstore.db import DB



class API_Sale(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, new_sale: schemas.sale.CreateSale) -> schemas.sale.ShowSaleWithSLIs:
        r = requests.post(f'{settings.host}/sale', data=new_sale.json(), headers=self.headers)
        if r.status_code != 201:
            raise ConnectionError(r.status_code)
        else:
            return schemas.sale.ShowSaleWithSLIs(**r.json())

    def update(self, sale_id: int, place_id: int, seller_id: int, date_time: datetime) -> schemas.sale.ShowSaleWithSLIs:
        pass

    def get_all(self) -> dict[int, schemas.sale.ShowSaleWithSLIs]:
        pass

    def get(self, sale_id: int) -> schemas.sale.ShowSaleWithSLIs:
        pass

    def delete(self, sale_id: int) -> bool:
        r = requests.delete(f"{settings.host}/sale/{sale_id}", headers=self.headers)
        if r.status_code != 204:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            return True
