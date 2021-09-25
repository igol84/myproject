import requests
from prjstore import schemas
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.db.api import settings
from prjstore.db import DB
from util.money import Money


def get_product(product_pd: schemas.product.Product) -> AbstractProduct:
    if product_pd.type == "shoes":
        product = ProductFactory.create(
            product_type=product_pd.type, prod_id=product_pd.id, name=product_pd.name,
            price=Money(product_pd.price), color=product_pd.shoes.color, size=product_pd.shoes.size,
            length_of_insole=product_pd.shoes.length, width=Shoes.widths[product_pd.shoes.width])
    else:
        product = ProductFactory.create(
            product_type="product", prod_id=product_pd.id,
            name=product_pd.name, price=(product_pd.price,))
    return product


class API_Product(DB):
    def __init__(self, headers):
        self.headers = headers

    def create(self, store_id: int, name: str) -> dict[int, AbstractProduct]:
        pass

    def update(self, seller_id: int, store_id: int, name: str) -> dict[int, AbstractProduct]:
        pass

    def get_all(self) -> dict[int, AbstractProduct]:
        r = requests.get(f"{settings.host}/prod", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            products_pd: list[schemas.product.Product] = schemas.product.ListProducts.parse_obj(r.json())
            products = {}
            for product_pd in products_pd:
                products[product_pd.id] = get_product(product_pd)
            return products

    def get(self, product_id: int) -> AbstractProduct:
        r = requests.get(f"{settings.host}/prod/{product_id}", headers=self.headers)
        if r.status_code != 200:
            err = r.json()['detail']
            raise ValueError(err.detail)
        else:
            product_pd = schemas.product.Product(**r.json())
            return get_product(product_pd)

    def delete(self, seller_id: int) -> bool:
        pass
