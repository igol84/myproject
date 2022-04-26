from prjstore.db.schemas import expense as schemas
from .base import APIBase, requests
from .. import settings


class API_Expense(APIBase[schemas.CreateExpense, schemas.UpdateExpense, schemas.Expense]):
    prefix = 'expense'
    schema = schemas.Expense
    list_schema = schemas.ListExpenses

    def __init__(self, headers):
        super().__init__(headers)

    def get_by_store_id(self, store_id: int) -> list[schemas.Expense]:
        r = requests.get(f"{settings.host}/{self.prefix}/{store_id}", headers=self.headers)
        if r.status_code != 200:
            raise ConnectionError(r.text)
        else:
            return list(self.list_schema.parse_obj(r.json()))
