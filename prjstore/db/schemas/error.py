from pydantic import BaseModel


class Err(BaseModel):
    detail: str
