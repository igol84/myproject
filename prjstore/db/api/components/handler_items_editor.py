import requests

from prjstore.db.api import settings
from prjstore.db.schemas import handler_items_editor as schemas


class API_HandlerItemEditor:
    prefix = 'handler_items_editor'

    def __init__(self, headers):
        self.headers = headers

    def edit_item(self, data: schemas.ItemFormEdit) -> schemas.ItemFormEdit:
        r = requests.put(f"{settings.host}/{self.prefix}/edit_item",
                         data=data.json(), headers=self.headers)
        if r.status_code != 201:
            raise ConnectionError(r.text)
        else:
            return schemas.ItemFormEdit(**r.json())

    def del_item(self, item_id: int) -> None:
        r = requests.delete(f"{settings.host}/{self.prefix}/del_item/{item_id}", headers=self.headers)
        if r.status_code != 204:
            raise ConnectionError(r.text)

    def get_item_sales(self, item_id: int) -> list[schemas.SaleDetail]:
        r = requests.get(f"{settings.host}/{self.prefix}/get_item_sales/{item_id}", headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            list_sales = []
            if r.json():
                list_sales = list(schemas.ListSaleDetail.parse_obj(r.json()))
            return list_sales
