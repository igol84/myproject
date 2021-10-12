from prjstore.db.api.components.base import APIBase
from prjstore.schemas.product_catalog import (CreateRowProductCatalog, ShowRowProductCatalogWithProduct,
                                              ProductCatalog)


class API_ProductCatalog(APIBase[CreateRowProductCatalog, CreateRowProductCatalog, ShowRowProductCatalogWithProduct]):
    prefix = 'product_catalog'
    schema = ShowRowProductCatalogWithProduct
    list_schema = ProductCatalog
    keys = ['store_id', 'prod_id']

    def __init__(self, headers):
        super().__init__(headers)
