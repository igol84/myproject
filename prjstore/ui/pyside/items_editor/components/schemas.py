from pydantic import BaseModel


class ViewItem(BaseModel):
    item_id: int
    desc: str
    price_buy: float
    sign: str = '₴'
    qty: int
    date_buy: str
    dates_of_sale: list[str] = []
