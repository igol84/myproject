from dataclasses import field

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.seller import Seller


@dataclass
class Store:
    factory: ProductFactory = ProductFactory()
    pc: ProductCatalog = ProductCatalog()
    items: dict[str, Item] = field(default_factory=dict)
    sellers: list[Seller] = field(default_factory=list)
    places_of_sale: list[PlaceOfSale] = field(default_factory=list)

    ###############################################################################################
    @validate_arguments
    def get_item_by_pr_id(self, pr_id: str) -> Item:
        if pr_id in self.items:
            return self.items[pr_id]
        raise IndexError(f"Invalid product id: {pr_id}")

    @validate_arguments
    def search_items_by_name(self, name: str = None) -> dict[str: Item]:
        items = {}
        if name:
            for it_id, item in self.items.items():
                if name.lower() in item.product.name.lower():
                    items[it_id] = item
        return items

    @validate_arguments
    def add_item(self, item: Item, qty: int = 1):
        if item.product.prod_id not in self.items:
            self.items[item.product.prod_id] = item
        self.items[item.product.prod_id].qty += qty
