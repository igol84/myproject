from dataclasses import field

from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.expense import Expense
from prjstore.domain.sale import Sale
from util.money import Money


@dataclass
class PlaceOfSale:
    id: int
    name: str
    ledger: dict[int, Sale] = field(default_factory=dict)
    expenses: dict[int, Expense] = field(default_factory=dict)
    active: bool = True
    sale: Sale = None

    def __hash__(self):
        return hash(self.id)

    def get_monthly_report(self) -> dict[(int, int), Money]:
        report = {}
        for sale in self.ledger.values():
            key = (sale.date_time.date().month, sale.date_time.date().year)
            if key in report:
                report[key] += sale.profit
            else:
                report[key] = sale.profit

        for expense in self.expenses.values():
            key = (expense.date_cost.month, expense.date_cost.year)
            if key in report:
                report[key] -= expense.cost
            else:
                report[key] = expense.cost
        return report

    @staticmethod
    def create_from_schema(schema: schemas.place.Place) -> 'PlaceOfSale':
        return PlaceOfSale(id=schema.id, name=schema.name, active=schema.active)
