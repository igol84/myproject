from prjstore.db.schemas import product as schemas
from prjstore.db.api.components.base import APIBase


class API_Product(APIBase[schemas.CreateProduct, schemas.Product, schemas.Product]):
    prefix = 'prod'
    schema = schemas.Product
    list_schema = schemas.ListProducts

    def __init__(self, headers):
        super().__init__(headers)
