import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_product_price_editor as schema
from prjstore.db.schemas.item import ShowItemWithProduct


class API_HandlerProductPriceEditor:
    prefix = 'handler_product_price_editor'

    def __init__(self, headers):
        self.headers = headers

    def edit_product(self, data: schema.ModelProduct) -> ShowItemWithProduct:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_product",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelProduct(**r.json())
