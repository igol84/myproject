from dataclasses import field

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from prjstore.db import schemas
from prjstore.domain.expense import Expense
from prjstore.domain.sale import Sale
from util.money import Money


class Report(BaseModel):
    head: str = ''
    total: Money = Money(0)
    expense: Money = Money(0)
    profit: Money = Money(0)

    def __add__(self, other: 'Report'):
        total = self.total + other.total
        expense = self.expense + other.expense
        profit = self.profit + other.profit
        return Report(head=self.head, total=total, expense=expense, profit=profit)


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

    def get_monthly_report(self) -> dict[(int, int), Report]:
        report = {}
        for sale in self.ledger.values():
            month = sale.date_time.date().month
            year = sale.date_time.date().year
            key = (month, year)
            if key in report:
                report[key].total += sale.total
                report[key].expense += sale.purchase
                report[key].profit += sale.profit
            else:
                head = f'{month:02}-{year}'
                report[key] = Report(head=head, total=sale.total, expense=sale.purchase, profit=sale.profit)

        for expense in self.expenses.values():
            month = expense.date_cost.month
            year = expense.date_cost.year
            key = (month, year)
            if key in report:
                report[key].expense += expense.cost
                report[key].profit -= expense.cost
            else:
                head = f'{month:02}-{year}'
                report[key] = Report(head=head, expense=expense.cost, profit=0 - expense.cost)
        return report

    def get_year_report(self) -> dict[int, Report]:
        year_report = {}
        for (month, year), report in self.get_monthly_report().items():
            if year in year_report:
                year_report[year] += report
            else:
                report.head = f'{year}'
                year_report[year] = report
        return year_report

    @staticmethod
    def create_from_schema(schema: schemas.place.Place) -> 'PlaceOfSale':
        return PlaceOfSale(id=schema.id, name=schema.name, active=schema.active)
