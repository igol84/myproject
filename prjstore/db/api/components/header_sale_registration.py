import requests

from prjstore.db.api import settings
from prjstore.db.schemas import header_sale_registration as schema


class API_HeaderSaleRegistration:
    prefix = 'header_sale_registration'

    def __init__(self, headers):
        self.headers = headers

    def edit_sli_price(self, data: schema.EditSLIPrice) -> schema.SaleLineItem:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_sli_price",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.SaleLineItem(**r.json())
