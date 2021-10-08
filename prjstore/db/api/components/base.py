from typing import TypeVar, Generic
from pydantic import BaseModel
import requests

from prjstore.db.api import settings
from prjstore.db import DB

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReceivedSchemaType = TypeVar("ReceivedSchemaType", bound=BaseModel)


class APIBase(DB, Generic[CreateSchemaType, UpdateSchemaType, ReceivedSchemaType]):
    prefix = None
    schema = None
    list_schema = None

    def __init__(self, headers):
        self.headers = headers

    def create(self, new_obj: CreateSchemaType) -> ReceivedSchemaType:
        r = requests.post(f'{settings.host}/{self.prefix}', json=new_obj.dict(), headers=self.headers)
        if r.status_code != 201:
            raise ConnectionError(r.status_code)
        else:
            return self.schema(**r.json())

    def update(self, new_obj: UpdateSchemaType) -> ReceivedSchemaType:
        r = requests.put(f"{settings.host}/{self.prefix}/{new_obj.id}", json=new_obj.dict(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.status_code)
        else:
            return self.schema(**r.json())

    def get_all(self) -> list[ReceivedSchemaType]:
        r = requests.get(f"{settings.host}/{self.prefix}", headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.status_code)
        else:
            return list(self.list_schema.parse_obj(r.json()))

    def get(self, obj_id: int) -> ReceivedSchemaType:
        r = requests.get(f"{settings.host}/{self.prefix}/{obj_id}", headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.status_code)
        else:
            return self.schema(**r.json())

    def delete(self, obj_id: int) -> bool:
        r = requests.delete(f"{settings.host}/item/{obj_id}", headers=self.headers)
        if r.status_code != 204:
            raise ConnectionError(r.status_code)
        else:
            return True
