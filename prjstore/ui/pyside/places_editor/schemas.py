from pydantic import BaseModel


class ViewPlace(BaseModel):
    place_id: int
    name: str
    active: bool = True
