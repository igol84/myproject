from pydantic.dataclasses import dataclass
from prjstore.domain.abstract_product import AbstractProduct


@dataclass
class SimpleProduct(AbstractProduct):
    product_type: str = 'product'
