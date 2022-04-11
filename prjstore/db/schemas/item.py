from datetime import date

from pydantic import BaseModel
from prjstore.db.schemas.product import Product


class BaseItem(BaseModel):
    prod_id: int
    store_id: int
    qty: int
    buy_price: float
    date_buy: date


class CreateItem(BaseItem):
    pass


class UpdateItem(BaseItem):
    id: int


class Item(BaseItem):
    id: int

    class Config:
        orm_mode = True


class ShowItemWithProduct(Item):
    product: Product


class ListItems(BaseModel):
    __root__: list[ShowItemWithProduct]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)

    def __len__(self):
        return len(self.__root__)
