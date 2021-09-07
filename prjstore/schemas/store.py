from pydantic import BaseModel


class BaseStore(BaseModel):
    name: str
    desc: str


class CreateStore(BaseStore):
    pass


class Store(BaseStore):
    id: int

    class Config:
        orm_mode = True


from prjstore.schemas.seller import Seller
from prjstore.schemas.place import Place
from prjstore.schemas.item import ShowItemWithProduct


class StoreWithDetails(Store):
    sellers: list[Seller]
    places: list[Place]
    items: list[ShowItemWithProduct]
