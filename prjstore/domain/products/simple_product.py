from pydantic.dataclasses import dataclass
from prjstore.domain.abstract_product import AbstractProduct


@dataclass
class SimpleProduct(AbstractProduct):
    product_type: str = 'product'

    def copy(self, prod_id=None) -> 'SimpleProduct':
        return SimpleProduct(prod_id=prod_id, product_type=self.product_type, name=self.name, price=self.price)
