from pydantic import BaseModel


class BaseSeller(BaseModel):
    store_id: int
    name: str
    active: bool


class CreateSeller(BaseSeller):
    pass


class UpdateSeller(CreateSeller):
    id: int


class Seller(BaseSeller):
    id: int

    class Config:
        orm_mode = True


class EditSellerName(BaseModel):
    seller_id: int
    new_name: str


class EditSellerActive(BaseModel):
    seller_id: int
    active: bool


class ListSeller(BaseModel):
    __root__: list[Seller]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
