from pydantic.dataclasses import dataclass


@dataclass
class Seller:
    id: int
    name: str
