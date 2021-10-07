from pydantic.dataclasses import dataclass

from prjstore.domain.sale import Sale


@dataclass
class PlaceOfSale:
    id: int
    name: str
    sale: Sale = None
