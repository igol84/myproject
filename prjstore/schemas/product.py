from typing import Optional

from pydantic import BaseModel

from prjstore.schemas.shoes import Shoes


class BaseProduct(BaseModel):
    type: str
    name: str
    price: float


class CreateProduct(BaseProduct):
    pass


class Product(BaseProduct):
    id: int
    shoes: Optional[Shoes] = None

    class Config:
        orm_mode = True


class ListProducts(BaseModel):
    __root__: list[Product]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
