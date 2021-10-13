from dataclasses import field

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.seller import Seller
from util.money import Money


@dataclass
class Store:
    id: int
    name: str
    factory: ProductFactory = ProductFactory()
    pc: ProductCatalog = ProductCatalog()
    items: dict[int, Item] = field(default_factory=dict)
    sellers: dict[int, Seller] = field(default_factory=dict)
    places_of_sale: dict[int, PlaceOfSale] = field(default_factory=dict)

    ###############################################################################################
    @validate_arguments
    def get_items_by_pr_id(self, pr_id: str) -> list[Item]:
        items = [_item for _item in self.items.values() if _item.product.prod_id == pr_id]
        if items:
            return items
        raise IndexError(f"Invalid product id: {pr_id}")

    @validate_arguments
    def search_items_by_name(self, name: str = None) -> dict[int: Item]:
        items = {}
        if name:
            for it_id, item in self.items.items():
                if name.lower() in item.product.name.lower():
                    items[it_id] = item
        return items

    @validate_arguments
    def add_item(self, item: Item, qty: int = 1):
        if item.id not in self.items:
            self.items[item.id] = item
        self.items[item.id].qty += qty

    @staticmethod
    def create_from_schema(schema: schemas.store.StoreWithDetails) -> 'Store':
        pc = ProductCatalog.create_from_schema(schema.products_catalog)
        items = {item.id: item for item in [Item.create_from_schema(item_pd) for item_pd in schema.items]}
        places = {place.id: place for place in [PlaceOfSale.create_from_schema(place_pd) for place_pd in schema.places]}
        sellers = {seller.id: seller for seller in
                   [Seller.create_from_schema(seller_pd) for seller_pd in schema.sellers]}
        return Store(id=schema.id, name=schema.name, pc=pc, items=items, places_of_sale=places, sellers=sellers)
