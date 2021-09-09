import requests

from prjstore.db import DB
from prjstore import schemas
from prjstore.domain.seller import Seller

from prjstore.db.api import settings
from prjstore.db.api.authorization import auth


class API_DB(DB):
    headers = auth()
    def create_seller(self, **kwargs) -> Seller:
        pass

    def update_seller(self, seller_id: int, **kwargs) -> Seller:
        pass

    def get_seller(self, seller_id: int) -> Seller:
        r = requests.get(f"{settings.host}/seller/{seller_id}", headers=self.headers)
        if (r.status_code != 200):
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            seller = schemas.seller.Seller(**r.json())
            return Seller(name=seller.name)

    def get_sellers(self) -> list[Seller]:
        pass

if __name__ == '__main__':
    db = API_DB()
    seller = db.get_seller(seller_id=2)
    print(seller)