import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_receiving_the_items as schema
from prjstore.db.schemas.item import ShowItemWithProduct


class API_HandlerReceivingTheItems:
    prefix = 'handler_receiving_the_item'

    def __init__(self, handlers):
        self.headers = handlers

    def receiving_the_items(self, data: schema.ModelProduct) -> ShowItemWithProduct:
        r = requests.put(f"{settings.host}/{self.prefix}/receiving_the_items",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
