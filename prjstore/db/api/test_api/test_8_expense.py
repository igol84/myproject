import datetime

from prjstore.db import API_DB, schemas
from prjstore.domain.expense import Expense

count_rows = 0
db = API_DB()


def setup_method():
    expenses: list = db.expense.get_all()
    global count_rows
    count_rows = len(expenses)


def teardown_method():
    expenses = db.expense.get_all()
    global count_rows
    assert count_rows == len(expenses), f" count expense changed '"


class TestPlace:
    obj_id: int = None

    @classmethod
    def setup_class(cls):
        pd_expense = schemas.expense.CreateExpense(place_id=1, desc='prom', date_cost=datetime.date(2022, 2, 24),
                                                   cost=100)
        new_expense = Expense.create_from_schema(db.expense.create(pd_expense))
        cls.obj_id = new_expense.id

    def test_case01_get(self):
        expense = Expense.create_from_schema(db.expense.get(self.obj_id))
        assert expense.desc == 'prom'

    def test_case02_update(self):
        pd_expense = schemas.expense.UpdateExpense(id=self.obj_id, place_id=1, desc='olx',
                                                   date_cost=datetime.date(2022, 2, 24), cost=100)
        expense = Expense.create_from_schema(db.expense.update(pd_expense))
        assert expense.desc == 'olx'

    @classmethod
    def teardown_class(cls):
        db.expense.delete(cls.obj_id)
