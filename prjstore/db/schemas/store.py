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


from prjstore.db.schemas.seller import Seller
from prjstore.db.schemas.place import Place
from prjstore.db.schemas.item import ShowItemWithProduct
from prjstore.db.schemas.product_catalog import ShowRowProductCatalogWithProduct


class StoreWithDetails(Store):
    sellers: list[Seller]
    places: list[Place]
    items: list[ShowItemWithProduct]
    products_catalog: list[ShowRowProductCatalogWithProduct]
