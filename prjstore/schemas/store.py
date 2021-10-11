from pydantic import BaseModel


class BaseStore(BaseModel):
    name: str
    desc: str


class CreateStore(BaseStore):
    pass


class UpdateStore(BaseStore):
    id: int


class Store(BaseStore):
    id: int

    class Config:
        orm_mode = True


from prjstore.schemas.seller import Seller
from prjstore.schemas.place import Place
from prjstore.schemas.item import ShowItemWithProduct
from prjstore.schemas.product_catalog import ShowProductCatalogWithProduct


class StoreWithDetails(Store):
    sellers: list[Seller]
    places: list[Place]
    items: list[ShowItemWithProduct]
    products_catalog: list[ShowProductCatalogWithProduct]
