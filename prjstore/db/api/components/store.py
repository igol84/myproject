import requests
from prjstore import schemas
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.seller import Seller
from prjstore.domain.store import Store
from prjstore.db.api import settings
from prjstore.db import DB
from util.money import Money


class API_Store(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, store_id: int, name: str) -> dict[int, Store]:
        pass

    def update(self, seller_id: int, store_id: int, name: str) -> dict[int, Store]:
        pass

    def get_all(self) -> dict[int, Store]:
        pass

    def get(self, store_id: int) -> Store:
        r = requests.get(f"{settings.host}/store/{store_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            store_pd = schemas.store.StoreWithDetails(**r.json())
            store = Store(id=store_pd.id, name=store_pd.name)
            for product in [product_catalog.product for product_catalog in store_pd.products_catalog]:
                store.pc.set_product(ProductFactory.create_from_schema(product))
            for item in store_pd.items:
                product = ProductFactory.create_from_schema(item.product)
                store.items[item.id] = Item(id=item.id, product=product, qty=item.qty, buy_price=Money(item.buy_price))
            for place in store_pd.places:
                store.places_of_sale[place.id] = PlaceOfSale(id=place.id, name=place.name)
            for seller in store_pd.sellers:
                store.sellers[seller.id] = Seller(id=seller.id, name=seller.name)
            return store

    def delete(self, seller_id: int) -> bool:
        pass
