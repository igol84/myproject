from typing import Optional

from prjstore.db import API_DB
from prjstore.db.schemas import expense as db_schemas
from prjstore.domain.store import Store
from prjstore.domain.expense import Expense
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.expenses_editor import schemas
from util.money import Money


class ExpenseHandler:
    __main_handler: Optional[MainHandler]
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, main_handler=None):
        self.__main_handler = main_handler
        self.__db = db
        self.store_id = self.db.headers['store_id']
        if not main_handler:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))

    def __get_main_handler(self) -> Optional[MainHandler]:
        return self.__main_handler

    def __set_main_handler(self, main_handler: MainHandler) -> None:
        self.__main_handler = main_handler

    main_handler = property(__get_main_handler, __set_main_handler)

    def __get_store(self):
        if self.main_handler:
            store = self.main_handler.store
        else:
            store = self.__store
        return store

    store = property(__get_store)

    def __get_db(self):
        if self.main_handler:
            db = self.main_handler.db
        else:
            db = self.__db
        return db

    db = property(__get_db)

    def get_places(self) -> dict[int, str]:
        return {place.id: place.name for place in self.store.places_of_sale.values()}

    def add_expense(self, pd_expense: schemas.FormNewExpense):
        # edit on DB
        pd_create_expense = db_schemas.CreateExpense(place_id=pd_expense.place_id, desc=pd_expense.desc,
                                                     date_cost=pd_expense.date_cost, cost=pd_expense.cost)
        pd_expense: db_schemas.Expense = self.db.expense.create(pd_create_expense)
        # edit in Domain Model
        expense = Expense(id=pd_expense.id, desc=pd_expense.desc, date_cost=pd_expense.date_cost,
                          cost=Money(pd_expense.cost))
        self.store.places_of_sale[pd_expense.place_id].expenses[pd_expense.id] = expense
        return pd_expense

    def edit_expense(self, pd_expense: schemas.ViewExpense):
        # edit on DB
        pd_update_expense = db_schemas.UpdateExpense(
            id=pd_expense.id,
            place_id=pd_expense.place_id,
            desc=pd_expense.desc,
            date_cost=pd_expense.date_cost,
            cost=pd_expense.cost
        )
        pd_expense: db_schemas.Expense = self.db.expense.update(pd_update_expense)
        # edit in Domain Model
        expense = Expense(id=pd_expense.id, desc=pd_expense.desc, date_cost=pd_expense.date_cost,
                          cost=Money(pd_expense.cost))
        self.store.places_of_sale[pd_expense.place_id].expenses[pd_expense.id] = expense
        return pd_expense

    def get_store_expenses(self) -> list[schemas.ViewExpense]:
        places = self.get_places()
        list_view = []
        list_pd_expenses = self.db.expense.get_by_store_id(store_id=self.store_id)
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

    def delete_expense(self, expense_id: int):
        # edit on DB
        self.db.expense.delete(expense_id)
        # edit in Domain Model
        for place in self.store.places_of_sale.values():
            if expense_id in place.expenses:
                del place.expenses[expense_id]
                break
