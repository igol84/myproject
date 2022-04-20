import datetime

from prjstore.domain.expense import Expense
from util.money import Money


class TestExpense:
    def setup(self) -> None:
        self.expenses = {1: Expense(1, 'prom', datetime.date(2022, 2, 24), Money(60)),
                         2: Expense(2, 'prom', datetime.date(2022, 2, 14), Money(140)),
                         3: Expense(3, 'prom', datetime.date(2022, 3, 24), Money(100))}


class Test_Seller(TestExpense):
    def test_01_initial(self):
        assert self.expenses[1].date_cost == datetime.date(2022, 2, 24)

    def test_02_edit_name(self):
        self.expenses[1].desc = 'olx'
        assert self.expenses[1].desc == 'olx'
