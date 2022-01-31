from typing import Optional

from pydantic import BaseModel


class BaseShoes(BaseModel):
    id: Optional[int] = None
    color: Optional[str] = None
    size: float
    length: Optional[float] = None
    width: Optional[str] = None


class UpdateShoes(BaseModel):
    color: str
    size: float
    length: float
    width: str


class CreateShoes(BaseShoes):
    pass


class CreateShoesWithProduct(UpdateShoes):
    pass


class Shoes(BaseShoes):
    pass

    class Config:
        orm_mode = True


class ListShoes(BaseModel):
    __root__: list[Shoes]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
