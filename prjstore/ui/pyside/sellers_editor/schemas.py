from pydantic import BaseModel


class ViewSeller(BaseModel):
    seller_id: int
    name: str
    active: bool = True

