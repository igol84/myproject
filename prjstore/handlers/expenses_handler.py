from prjstore.db import API_DB
from prjstore.db.schemas import expense as db_schemas
from prjstore.domain.store import Store
from prjstore.domain.expense import Expense
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.expenses_editor import schemas
from util.money import Money


class ExpenseHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, store=None):
        self.__db = db
        if test:
            self.__store = Store(id=1, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.store_id = db.headers['store_id']
            self.update_data(store)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def update_data(self, store: Store):
        if not store:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))
        else:
            self.__store = store

    def get_places(self) -> dict[int, str]:
        return {place.id: place.name for place in self.store.places_of_sale.values()}

    def add_expense(self, pd_expense: schemas.FormNewExpense):
        # edit on DB
        pd_create_expense = db_schemas.CreateExpense(place_id=pd_expense.place_id, desc=pd_expense.desc,
                                                     date_cost=pd_expense.date_cost, cost=pd_expense.cost)
        pd_expense: db_schemas.Expense = self.__db.expense.create(pd_create_expense)
        # edit in Domain Model
        expense = Expense(id=pd_expense.id, desc=pd_expense.desc, date_cost=pd_expense.date_cost,
                          cost=Money(pd_expense.cost))
        self.store.places_of_sale[pd_expense.place_id].expenses[pd_expense.id] = expense
        return pd_expense

    def get_store_expenses(self) -> list[schemas.ViewExpense]:
        places = self.get_places()
        list_view = []
        list_pd_expenses = self.__db.expense.get_by_store_id(store_id=self.store_id)
        for pd_expense in list_pd_expenses:
            expense = Expense.create_from_schema(pd_expense)
            # update domain
            self.store.places_of_sale[pd_expense.place_id].expenses[expense.id] = expense
            # get view data
            view = schemas.ViewExpense(id=pd_expense.id, places=places, place_id=pd_expense.place_id,
                                       desc=pd_expense.desc, date_cost=pd_expense.date_cost, cost=pd_expense.cost)
            list_view.append(view)
            list_view.sort(key=lambda k: k.id, reverse=True)
        return list_view
