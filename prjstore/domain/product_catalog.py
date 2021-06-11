from dataclasses import field

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from util.money import Money


@dataclass
class ProductCatalog:
    products: dict[str, AbstractProduct] = field(init=False, default_factory=dict)

    ###############################################################################################
    @validate_arguments
    def set_product(self, pr: AbstractProduct) -> None:
        self.products[pr.prod_id] = pr

    @validate_arguments
    def unset_product_by_pr_id(self, pr_id: str) -> None:
        del self.products[pr_id]

    @validate_arguments
    def __delitem__(self, prod_id: str) -> None:
        self.unset_product_by_pr_id(prod_id)

    @validate_arguments
    def get_product_by_id(self, prod_id: str) -> AbstractProduct:
        if prod_id in self.products:
            return self.products[prod_id]
        raise IndexError(f"Invalid product id: {prod_id}")

    @validate_arguments
    def __getitem__(self, prod_id: str) -> AbstractProduct:
        return self.get_product_by_id(prod_id)

    @validate_arguments
    def search(self, name: str = None) -> dict[str, AbstractProduct]:
        products = {}
        if name:
            for product in self.products.values():
                if name.lower() in product.name.lower():
                    products[product.prod_id] = product
        return products
