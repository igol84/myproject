from prjstore.schemas import seller as schemas
from prjstore.db.api.components.base import APIBase


class API_Seller(APIBase[schemas.CreateSeller, schemas.UpdateSeller, schemas.Seller]):
    prefix = 'seller'
    schema = schemas.Seller
    list_schema = schemas.ListSeller

    def __init__(self, headers):
        super().__init__(headers)
