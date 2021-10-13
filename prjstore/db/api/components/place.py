from prjstore.db.schemas import place as schemas
from prjstore.db.api.components.base import APIBase


class API_Place(APIBase[schemas.CreatePlace, schemas.UpdatePlace, schemas.Place]):
    prefix = 'place'
    schema = schemas.Place
    list_schema = schemas.ListPlace

    def __init__(self, headers):
        super().__init__(headers)
