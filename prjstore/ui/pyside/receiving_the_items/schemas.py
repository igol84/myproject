from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ModelItem(BaseModel):
    id: Optional[int] = None
    prod_id: Optional[int] = None
    price_buy: Optional[float] = None
    qty: Optional[int] = None


class ModelSizeShoes(BaseModel):
    size: Optional[float] = None
    length: Optional[float] = None
    qty: Optional[int] = None


class ModelColorShoes(BaseModel):
    color: Optional[str] = None
    width: Optional[str] = None
    sizes: dict[float, ModelSizeShoes] = {}


class Type(Enum):
    simple = 'simple'
    shoes = 'shoes'


class ModelProduct(BaseModel):
    id: int
    type: Type = Type.simple
    name: str
    price_sell: float
    shoes: Optional[ModelColorShoes] = None
