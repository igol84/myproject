from pydantic.dataclasses import dataclass

from prjstore.domain.sale import Sale

@dataclass
class PlaceOfSale:
    name: str
    sale: Sale = None