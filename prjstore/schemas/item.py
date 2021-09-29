from pydantic import BaseModel
from prjstore.schemas.product import Product


class BaseItem(BaseModel):
    prod_id: int
    store_id: int
    qty: int
    buy_price: float


class CreateItem(BaseItem):
    pass


class Item(BaseItem):
    id: int

    class Config:
        orm_mode = True


class ShowItemWithProduct(Item):
    product: Product


class ViewItem(BaseModel):
    prod_id: int
    name: str
    price: float
    price_format: str
    qty: int

class ListItems(BaseModel):
    __root__: list[Item]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
