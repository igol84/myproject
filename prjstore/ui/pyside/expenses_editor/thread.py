from PySide6.QtCore import Signal, QObject, QRunnable, Slot
from pydantic import ValidationError

from prjstore.db import API_DB
from prjstore.db.schemas import expense as schemas
from prjstore.handlers.expenses_handler import ExpenseHandler
from prjstore.ui.pyside.expenses_editor import schemas


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ExpenseHandler)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = ExpenseHandler(db)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(handler)


class DBAddExpense(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: ExpenseHandler, pd_data: schemas.FormNewExpense):
        super().__init__()
        self.handler = handler
        self.pd_data = pd_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.add_expense(self.pd_data)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        except ValidationError as e:
            fields = {'place_id': 'место', 'cost': 'стоимость'}
            warning = ''
            for r in e.raw_errors:
                for field in fields:
                    if r.loc_tuple()[0] == field:
                        warning += f'Поле "{fields[field]}" не выбрано\n'
            self.signals.error.emit(warning)
        else:
            self.signals.complete.emit()


class DBDelExpense(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: ExpenseHandler, expense_id: int):
        super().__init__()
        self.handler = handler
        self.expense_id = expense_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.delete_expense(self.expense_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()


class DBEditExpense(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(schemas.ViewExpense)

    def __init__(self, handler: ExpenseHandler, pd_data: schemas.ViewExpense):
        super().__init__()
        self.handler = handler
        self.pd_data = pd_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_data: schemas.Expense = self.handler.edit_expense(self.pd_data)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        except ValidationError as e:
            fields = {'place_id': 'место', 'cost': 'стоимость'}
            warning = ''
            for r in e.raw_errors:
                for field in fields:
                    if r.loc_tuple()[0] == field:
                        warning += f'Поле "{fields[field]}" не выбрано\n'
            self.signals.error.emit(warning)
        else:
            places = self.handler.get_places()
            pd_view = schemas.ViewExpense(id=pd_data.id, place_id=pd_data.place_id, desc=pd_data.desc,
                                          date_cost=pd_data.date_cost, cost=pd_data.cost, places=places)
            self.signals.result.emit(pd_view)
