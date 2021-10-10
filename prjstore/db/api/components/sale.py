import requests
from prjstore.db.api.components.base import APIBase
from prjstore.schemas import sale as schemas
from prjstore.db.api import settings


class API_Sale(APIBase[schemas.CreateSale, schemas.UpdateSale, schemas.ShowSaleWithSLIs]):
    prefix = 'sale'
    schema = schemas.ShowSaleWithSLIs
    list_schema = schemas.ListSale

    def __init__(self, headers):
        super().__init__(headers)

    def update(self, new_obj: schemas.UpdateSale) -> schemas.ShowSaleWithSLIs:
        r = requests.put(f"{settings.host}/{self.prefix}/",
                         data=new_obj.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return self.schema(**r.json())
