import requests

from prjstore.db.api import settings
from prjstore.db.schemas import header_receiving_the_items as schema
from prjstore.db.schemas.item import ShowItemWithProduct


class API_HeaderReceivingTheItems:
    prefix = 'handler_receiving_the_item'

    def __init__(self, headers):
        self.headers = headers

    def receiving_the_items(self, data: schema.ModelProduct) -> ShowItemWithProduct:
        r = requests.put(f"{settings.host}/{self.prefix}/receiving_the_items",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
