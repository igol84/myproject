from pydantic.dataclasses import dataclass
from prjstore.db import schemas


@dataclass
class Seller:
    id: int
    name: str

    @staticmethod
    def create_from_schema(schema: schemas.seller.Seller) -> 'Seller':
        return Seller(id=schema.id, name=schema.name)
