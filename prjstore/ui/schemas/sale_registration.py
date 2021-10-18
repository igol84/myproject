from typing import Optional

from pydantic import BaseModel


class ViewShoes(BaseModel):
    size: float
    color: Optional[str] = None
    length: Optional[float] = None
    width: Optional[str] = None

class ViewItem(BaseModel):
    prod_id: int
    name: str
    price: float
    price_format: str
    qty: int
    type: Optional[str] = None
    shoes: Optional[ViewShoes] = None