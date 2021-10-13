from prjstore.db.schemas import item as schemas
from .base import APIBase


class API_Item(APIBase[schemas.CreateItem, schemas.UpdateItem, schemas.ShowItemWithProduct]):
    prefix = 'item'
    schema = schemas.ShowItemWithProduct
    list_schema = schemas.ListItems

    def __init__(self, headers):
        super().__init__(headers)
