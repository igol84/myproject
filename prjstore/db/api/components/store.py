from prjstore.db.api.components.base import APIBase
from prjstore.db.schemas import store as schemas


class API_Store(APIBase[schemas.CreateStore, schemas.UpdateStore, schemas.StoreWithDetails]):
    prefix = 'store'
    schema = schemas.StoreWithDetails
    list_schema = schemas.ListStore

    def __init__(self, headers):
        super().__init__(headers)
