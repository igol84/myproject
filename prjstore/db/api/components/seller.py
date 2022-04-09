import requests

from prjstore.db.api import settings
from prjstore.db.schemas import seller as schemas
from prjstore.db.api.components.base import APIBase


class API_Seller(APIBase[schemas.CreateSeller, schemas.UpdateSeller, schemas.Seller]):
    prefix = 'seller'
    schema = schemas.Seller
    list_schema = schemas.ListSeller

    def __init__(self, headers):
        super().__init__(headers)

    def edit_name(self, seller_id: int, new_name: str) -> schemas.Seller:
        data = schemas.EditSellerName(seller_id=seller_id, new_name=new_name)
        r = requests.put(f"{settings.host}/{self.prefix}/edit_name",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schemas.Seller(**r.json())

    def edit_active(self, seller_id: int, active: bool) -> schemas.Seller:
        data = schemas.EditSellerActive(seller_id=seller_id, active=active)
        r = requests.put(f"{settings.host}/{self.prefix}/edit_active",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schemas.Seller(**r.json())
