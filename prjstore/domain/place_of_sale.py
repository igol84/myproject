from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.sale import Sale


@dataclass
class PlaceOfSale:
    id: int
    name: str
    sale: Sale = None

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def create_from_schema(schema: schemas.place.Place) -> 'PlaceOfSale':
        return PlaceOfSale(id=schema.id, name=schema.name)
