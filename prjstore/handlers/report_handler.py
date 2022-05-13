from enum import Enum
from typing import Optional

from prjstore.db import API_DB
from prjstore.domain.expense import Expense
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.handlers.abstract_module_handler import AbstractModuleHandler
from prjstore.handlers.main_handler import MainHandler


class ReportHandler(AbstractModuleHandler):
    db: API_DB
    store: Store

    def __init__(self, db: API_DB = None, main_handler: MainHandler = None):
        super().__init__(db, main_handler)

    def get_places(self) -> dict[int, str]:
        return {place.id: place.name for place in self.store.places_of_sale.values()}

    def setup_store_expenses(self) -> None:
        list_pd_expenses = self.db.expense.get_by_store_id(store_id=self.store.id)
        for pd_expense in list_pd_expenses:
            expense = Expense.create_from_schema(pd_expense)
            # update domain
            self.store.places_of_sale[pd_expense.place_id].expenses[expense.id] = expense

    def setup_store_ledger(self):
        places = self.get_places()
        for place_id in places:
            pd_sales = self.db.sale.get_all(place_id=place_id)
            for pd_sale in pd_sales:
                sale = Sale.create_from_schema(pd_sale)
                # update domain
                self.store.places_of_sale[place_id].ledger[sale.id] = sale

    class Range(Enum):
        month = 'мес.'
        year = 'год.'

    def get_report(self, range: Range, place_id: Optional[int] = None):
        if not place_id:
            if range == self.Range.month:
                return self.store.get_monthly_report()
            if range == self.Range.year:
                return self.store.get_year_report()
        else:
            if range == self.Range.month:
                return self.store.places_of_sale[place_id].get_monthly_report()
            if range == self.Range.year:
                return self.store.places_of_sale[place_id].get_year_report()