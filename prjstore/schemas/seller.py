from pydantic import BaseModel


class BaseSeller(BaseModel):
    store_id: int
    name: str


class CreateSeller(BaseSeller):
    pass


class Seller(BaseSeller):
    id: int

    class Config:
        orm_mode = True


class ListSeller(BaseModel):
    __root__: list[Seller]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)