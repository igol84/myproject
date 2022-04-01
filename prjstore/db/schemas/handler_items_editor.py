from pydantic import BaseModel


class ItemForm(BaseModel):
    id: int
    new_qty: int
    new_price: float
