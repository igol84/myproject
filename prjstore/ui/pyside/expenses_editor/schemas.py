import datetime
from typing import Optional

from pydantic import BaseModel


class ViewNewExpense(BaseModel):
    places: dict[int, str]
    date: datetime.date = datetime.date.today()


class FormNewExpense(BaseModel):
    place_id: Optional[int]
    desc: str
    date_cost: datetime.date = datetime.date.today()
    cost: Optional[float]


class ViewExpense(BaseModel):
    id: int
    places: dict[int, str]
    place_id: Optional[int]
    desc: str
    date_cost: datetime.date = datetime.date.today()
    cost: Optional[float]
    sign: str = '₴'
