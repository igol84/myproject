import datetime
from typing import Optional

from pydantic import BaseModel


class ViewItem(BaseModel):
    item_id: int
    desc: str
    price_buy: float
    sign: str = '₴'
    qty: int
    date_buy: datetime.date
    dates_of_sale: Optional[list[str]] = None
