from typing import Optional

from pydantic import BaseModel


class ModelShoes(BaseModel):
    size: float
    color: Optional[str] = None
    length: Optional[float] = None
    width: Optional[str] = None
    width_of_insole: Optional[float] = None


class ModelProduct(BaseModel):
    prod_id: str
    name: str
    price: float
    price_format: str
    qty: int
    type: str = ''
    shoes: Optional[ModelShoes] = None

    def get_desc(self) -> str:
        if self.shoes:
            desc = self.name
            desc += f' {self.shoes.color}' if self.shoes.color else ''
            desc += f' {self.shoes.width}' if self.shoes.width else ''
            desc += f' {self.shoes.size:g}'
        else:
            desc = self.name
        return desc


class ProductId(str):
    pass


class Price(float):
    pass


class ViewProduct(ModelProduct):
    pass


class ViewSize(BaseModel):
    prod_id: str
    size: float
    price: float
    price_format: str
    qty: int


class ViewWidth(BaseModel):
    width: Optional[str] = None
    sizes: list[ViewSize]


class ViewColor(BaseModel):
    color: Optional[str] = None
    widths: list[ViewWidth]


class ViewShoes(BaseModel):
    type: str = 'shoes'
    name: str
    colors: list[ViewColor]
