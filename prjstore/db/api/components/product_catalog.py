import requests

from prjstore.db.api import settings
from prjstore.db.api.components.base import APIBase
from prjstore.db.schemas.product_catalog import (CreateRowProductCatalog, ShowRowProductCatalogWithProduct,
                                                 ProductCatalog)


class API_ProductCatalog(APIBase[CreateRowProductCatalog, CreateRowProductCatalog, ShowRowProductCatalogWithProduct]):
    prefix = 'product_catalog'
    schema = ShowRowProductCatalogWithProduct
    list_schema = ProductCatalog
    keys = ['store_id', 'prod_id']

    def __init__(self, headers):
        super().__init__(headers)

    def get_store_pc(self, store_id: int) -> list[ShowRowProductCatalogWithProduct]:
        r = requests.get(f"{settings.host}/{self.prefix}/{store_id}", headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.text)
        else:
            return list(self.list_schema.parse_obj(r.json()))
