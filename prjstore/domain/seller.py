from pydantic.dataclasses import dataclass
from prjstore.db import schemas


@dataclass
class Seller:
    id: int
    name: str
    active: bool = False

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def create_from_schema(schema: schemas.seller.Seller) -> 'Seller':
        return Seller(id=schema.id, name=schema.name, active=schema.active)
