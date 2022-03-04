import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_sale_registration as schema


class API_HandlerSaleRegistration:
    prefix = 'handler_sale_registration'

    def __init__(self, headers):
        self.headers = headers

    def edit_sli_price(self, data: schema.EditSLIPrice):
        r = requests.put(f"{settings.host}/{self.prefix}/edit_sli_price",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)

    def put_items_from_old_sale(self, data: schema.PutItemFromOldSale) -> None:
        r = requests.put(f"{settings.host}/{self.prefix}/put_item_from_old_sale",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
