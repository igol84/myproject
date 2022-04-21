from datetime import date
from prjstore.db import schemas
from pydantic.dataclasses import dataclass

from util.money import Money


@dataclass
class Expense:
    id: int = None
    desc: str = ''
    date_cost: date = date.today()
    cost: Money = Money(0)

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def create_from_schema(schema: schemas.expense.Expense) -> 'Expense':
        return Expense(id=schema.id, desc=schema.desc, date_cost=schema.date_cost, cost=Money(schema.cost))
