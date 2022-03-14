import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_product_price_editor as schema


class API_HandlerProductPriceEditor:
    prefix = 'handler_product_price_editor'

    def __init__(self, headers):
        self.headers = headers

    def edit_product(self, data: schema.ModelProductForm) -> schema.ModelProductForm:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_product",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelProductForm(**r.json())

    def edit_size(self, data: schema.ModelSize) -> schema.ModelSize:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_size",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelSize(**r.json())

    def edit_shoes(self, data: schema.ModelShoes) -> schema.ModelShoes:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_shoes",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelShoes(**r.json())

    def edit_color(self, data: schema.ModelColor) -> schema.ModelColor:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_color",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelColor(**r.json())