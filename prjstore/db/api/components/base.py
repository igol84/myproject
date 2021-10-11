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
    keys = ['id']

    def __init__(self, headers):
        self.headers = headers

    def create(self, new_obj: CreateSchemaType) -> ReceivedSchemaType:
        r = requests.post(f'{settings.host}/{self.prefix}', data=new_obj.json(), headers=self.headers)
        if r.status_code != 201:
            raise ConnectionError(r.text)
        else:
            return self.schema(**r.json())

    def update(self, new_obj: UpdateSchemaType) -> ReceivedSchemaType:
        r = requests.put(f"{settings.host}/{self.prefix}/",
                         data=new_obj.json(), headers=self.headers)
        if r.status_code != 202:
            raise ConnectionError(r.text)
        else:
            return self.schema(**r.json())

    def get_all(self) -> list[ReceivedSchemaType]:
        r = requests.get(f"{settings.host}/{self.prefix}", headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.text)
        else:
            return list(self.list_schema.parse_obj(r.json()))

    def get(self, *args, **kwargs) -> ReceivedSchemaType:
        r = requests.get(f"{settings.host}/{self.prefix}/{self.create_key_by_args(*args, **kwargs)}",
                         headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.text)
        else:
            return self.schema(**r.json())

    def delete(self, *args, **kwargs) -> bool:
        r = requests.delete(f"{settings.host}/{self.prefix}/{self.create_key_by_args(*args, **kwargs)}",
                            headers=self.headers)
        if r.status_code != 204:
            raise ConnectionError(r.text)
        else:
            return True

    def create_key_by_schemas(self, obj):
        return '/'.join([str(getattr(obj, key)) for key in self.keys])

    def create_key_by_args(self, *args, **kwargs):
        obj = {}
        if args:
            obj = dict(zip(self.keys, args))
        if kwargs:
            obj = kwargs
        return '/'.join([str(obj[key]) for key in self.keys])
