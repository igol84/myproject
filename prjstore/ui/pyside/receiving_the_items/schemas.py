from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ModelSizeShoes(BaseModel):
    size: Optional[float] = None
    length: Optional[float] = None


class ModelColorShoes(BaseModel):
    color: Optional[str] = None
    width: Optional[str] = None
    sizes: list[ModelSizeShoes] = []

class Type(Enum):
    simple = 'simple'
    shoes = 'shoes'

class ModelItem(BaseModel):
    id: Optional[int] = None
    prod_id: Optional[int] = None
    qty: Optional[int] = None
    buy_price: Optional[float] = None
    name: Optional[str] = None
    price: Optional[float] = None
    type: Type = Type.simple
    shoes: Optional[ModelColorShoes] = None


