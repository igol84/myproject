from prjstore.db.api.components.base import APIBase
from prjstore.schemas import sale as schemas


class API_Sale(APIBase[schemas.CreateSale, schemas.UpdateSale, schemas.ShowSaleWithSLIs]):
    prefix = 'sale'
    schema = schemas.ShowSaleWithSLIs
    list_schema = schemas.ListSale

    def __init__(self, headers):
        super().__init__(headers)
