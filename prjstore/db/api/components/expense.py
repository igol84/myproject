from prjstore.db.schemas import expense as schemas
from .base import APIBase


class API_Expense(APIBase[schemas.CreateExpense, schemas.UpdateExpense, schemas.Expense]):
    prefix = 'expense'
    schema = schemas.Expense
    list_schema = schemas.ListExpenses

    def __init__(self, headers):
        super().__init__(headers)
