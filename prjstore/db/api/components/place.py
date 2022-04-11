import requests

from prjstore.db.api import settings
from prjstore.db.schemas import place as schemas
from prjstore.db.api.components.base import APIBase


class API_Place(APIBase[schemas.CreatePlace, schemas.UpdatePlace, schemas.Place]):
    prefix = 'place'
    schema = schemas.Place
    list_schema = schemas.ListPlace

    def __init__(self, headers):
        super().__init__(headers)

    def edit_name(self, place_id: int, new_name: str) -> schemas.Place:
        data = schemas.EditPlaceName(place_id=place_id, new_name=new_name)
        r = requests.put(f"{settings.host}/{self.prefix}/edit_name",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schemas.Place(**r.json())

    def edit_active(self, place_id: int, active: bool) -> schemas.Place:
        data = schemas.EditPlaceActive(place_id=place_id, active=active)
        r = requests.put(f"{settings.host}/{self.prefix}/edit_active",
                         data=data.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return schemas.Place(**r.json())
