import sys
from typing import Optional

from prjstore.handlers.expenses_handler import ExpenseHandler
from prjstore.ui.pyside.expenses_editor import thread
from prjstore.ui.pyside.expenses_editor.components.add_expense_widget import AddExpenseWidget
from prjstore.ui.pyside.expenses_editor import schemas
from prjstore.ui.pyside.expenses_editor.components.expense_widget import ExpenseWidget
from prjstore.ui.pyside.expenses_editor.schemas import ViewNewExpense
from prjstore.ui.pyside.expenses_editor.ui_expenses import UI_Expenses
from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class ExpensesEditor(QWidget, ObserverInterface):
    __pd_expenses: list[schemas.ViewExpense]
    __selected_expense_id: Optional[int]
    __add_expense_widget: AddExpenseWidget
    __expense_widgets: dict[int, ExpenseWidget]
    __handler: ExpenseHandler
    __dark_style: bool

    def __init__(self, parent=None, test=False, user_data=None, list_pd_expenses=None, db=None, dark_style=False):
        super().__init__()
        self.parent: MainWindowInterface = parent
        if parent:
            self.parent.register_observer(self)
        self.__handler = None
        self.test = test
        self.need_update: bool = True
        self.ui = UI_Expenses()
        self.ui.setup_ui(self)
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.dark_style = dark_style
        if list_pd_expenses is None:
            list_pd_expenses = []
        self.list_pd_expenses: list = list_pd_expenses
        self.__selected_expense_id = None
        self.__expense_widgets = {}
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.parent:
            if not self.test:
                db_connector = thread.DbConnect(self.user_data, self.db)
                db_connector.signals.error.connect(self.__connection_error)
                db_connector.signals.result.connect(self.__connected_complete)
                self.thread_pool.start(db_connector)
            else:
                self.__connected_complete(ExpenseHandler(db=None, test=True))
        else:
            store = self.parent.handler.store
            self.__connected_complete(ExpenseHandler(db=self.db, store=store))

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        self.load_widget.hide()

    def __connected_complete(self, handler: ExpenseHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def get_selected_expense_id(self) -> int:
        return self.__selected_expense_id

    def set_selected_expense_id(self, selected_expense_id: Optional[int]) -> None:
        if self.selected_expense_id:
            self.selected_widget.selected = False
        if selected_expense_id is not None:
            self.__selected_expense_id = selected_expense_id
            self.selected_widget.selected = True
        else:
            self.__selected_expense_id = None

    selected_expense_id = property(get_selected_expense_id, set_selected_expense_id)

    def get_selected_widget(self) -> ExpenseWidget:
        if self.selected_expense_id:
            return self.__expense_widgets[self.selected_expense_id]

    selected_widget = property(get_selected_widget)

    def get_dark_style(self) -> bool:
        return self.__dark_style

    def set_dark_style(self, flag: bool) -> None:
        self.__dark_style = flag
        if flag:
            self.setStyleSheet(
                '#ExpensesEditor, #ExpensesFrame {background-color: #2F303B; color: #F8F8F2;}\n'
                '#ExpensesEditor #Title {color: #F8F8F2;}\n'
            )

    dark_style = property(get_dark_style, set_dark_style)

    def update_data(self, store=None) -> None:
        if self.need_update:
            self.load_widget.show()
            self.handler.update_data(store)
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self) -> None:
        clearLayout(self.ui.layout_expenses)
        places = self.handler.get_places()
        data = ViewNewExpense(places=places)
        self.__add_expense_widget = AddExpenseWidget(self, data)
        self.ui.layout_expenses.addWidget(self.__add_expense_widget)

        self.__pd_expenses = self.handler.get_store_expenses()
        for pd_expense in self.__pd_expenses:
            item_frame = ExpenseWidget(pd_expense, self)
            self.__expense_widgets[pd_expense.id] = item_frame
            self.ui.layout_expenses.addWidget(item_frame)
        if self.selected_expense_id:
            self.set_selected_expense_id(self.selected_expense_id)

    def on_add_expense(self, pd_data: schemas.FormNewExpense):
        self.load_widget.show()
        db_expense = thread.DBAddExpense(self.handler, pd_data)
        db_expense.signals.error.connect(self.__connection_error)
        db_expense.signals.result.connect(self.__adding_expense_complete)
        self.thread_pool.start(db_expense)

    def __adding_expense_complete(self, pd_new_expense: schemas.ViewExpense):
        self.__add_expense_widget.clear()
        item_frame = ExpenseWidget(pd_new_expense, self)
        self.__expense_widgets[pd_new_expense.id] = item_frame
        self.ui.layout_expenses.insertWidget(1, item_frame)
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ExpensesEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
