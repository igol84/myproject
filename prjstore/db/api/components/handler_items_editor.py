import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_items_editor as schema


class API_HandlerItemEditor:
    prefix = 'handler_items_editor'

    def __init__(self, headers):
        self.headers = headers

    def edit_item(self, data: schema.ItemFormEdit) -> schema.ItemFormEdit:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_item",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schema.ItemFormEdit(**r.json())

    def del_item(self, data: schema.ItemFormDel) -> None:
        r = requests.put(f"{settings.host}/{self.prefix}/del_item",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
