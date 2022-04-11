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

    def edit_size(self, data: schema.ModelSizeForm) -> schema.ModelSizeForm:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_size",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelSizeForm(**r.json())

    def edit_shoes(self, data: schema.ModelShoesForm) -> schema.ModelShoesForm:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_shoes",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelShoesForm(**r.json())

    def edit_color(self, data: schema.ModelColorForm) -> schema.ModelColorForm:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_color",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ModelColorForm(**r.json())