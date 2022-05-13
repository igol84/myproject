import datetime
import sys

from prjstore.db import API_DB
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.main_items_editor import ItemsEditor
from prjstore.ui.pyside.main_login import LoginFrame
from prjstore.ui.pyside.main_places import PlacesEditor
from prjstore.ui.pyside.main_expenses import ExpensesEditor
from prjstore.ui.pyside.main_product_price_editor import PriceEditor
from prjstore.ui.pyside.main_receiving_the_items import ItemForm
from prjstore.ui.pyside.main_report import ReportPage
from prjstore.ui.pyside.main_sale_registration import SaleForm
from prjstore.ui.pyside.main_sellers import SellersEditor
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.main_window.thread import DbConnect
from prjstore.ui.pyside.main_window.ui_main_window import UI_MainWindow
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.push_button import PyPushBottom
from prjstore.ui.pyside.utils.qt_core import *


class MainWindow(QMainWindow, MainWindowInterface):
    handler: MainHandler
    moduls: dict[AbstractModule]
    observers: list
    dark_style: bool
    ui: UI_MainWindow

    def __init__(self):
        super().__init__()
        self.moduls = {}
        self.observers = []
        self.handler = None
        self.dark_style = True
        self.ui = None

        self.thread_pool = QThreadPool()
        self.login_form = LoginFrame(self)
        module_names = ['new_items_form', 'edit_items_form', 'price_editor_form', 'sale_form', 'sellers_form',
                        'places_form', 'expenses_form', 'report_page']
        self.moduls = dict.fromkeys(module_names)
        self.setup_ui()
        self.start_connection()

    def register_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        del self.observers[observer]

    def notify_observer(self, this_observer: AbstractModule) -> None:
        for observer in self.observers:
            if observer.name in this_observer.observer_module_names:
                observer.need_update = True

    def data_changed(self, this_observer) -> None:
        self.notify_observer(this_observer)

    def on_receiving_data_change(self, this_observer):
        self.data_changed(this_observer)
        self.moduls['edit_items_form'].update_data()

    def setup_ui(self):
        self.setWindowTitle('Shop')
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.ui.setup_login_module(self.login_form)
        self.ui.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.show()

    def start_connection(self):
        self.ui.load_widget.show()
        db_connector = DbConnect(self.login_form.get_user_data())
        db_connector.signals.connection_error.connect(self.__connection_error)
        db_connector.signals.authentication_error.connect(self.__authentication_error)
        db_connector.signals.result.connect(self.__connected_complete)
        self.thread_pool.start(db_connector)

    def __connection_error(self, err: str, desc: str):
        QMessageBox.warning(self, err, desc)
        sys.exit(app.exec())

    def __authentication_error(self, err: str):
        self.setup_ui()
        self.show_login_page()
        self.ui.load_widget.hide()
        QMessageBox.warning(self, err, err)

    def __connected_complete(self, db: API_DB):
        for module in self.moduls:
            self.moduls[module] = None
        self.handler = MainHandler(db)
        self.setWindowTitle(f'Shop - {self.login_form.name}')

        self.ui.btn_new_items.clicked.connect(self.show_items_page)
        self.ui.btn_price_editor.clicked.connect(self.show_product_price_editor_page)
        self.ui.btn_sale.clicked.connect(self.show_sale_registration_page)
        self.ui.btn_sellers.clicked.connect(self.show_sellers_places_page)
        self.ui.btn_expenses.clicked.connect(self.show_expenses_page)
        self.ui.btn_report.clicked.connect(self.show_report_page)
        self.ui.login_button.clicked.connect(self.show_login_page)
        self.ui.settings_button.clicked.connect(self.show_settings_page_page)
        self.show_sale_registration_page()
        self.ui.load_widget.hide()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if isinstance(btn, PyPushBottom):
                btn.set_active(False)

    def show_page(self, btn, page):
        self.reset_selection()
        btn.set_active(True)
        self.ui.pages.setCurrentWidget(page)

    def show_items_page(self):
        if self.moduls['new_items_form'] is None and self.moduls['edit_items_form'] is None:
            self.moduls['new_items_form'] = ItemForm(self)
            self.moduls['edit_items_form'] = ItemsEditor(self)
            self.ui.setup_items_form(self.moduls['new_items_form'], self.moduls['edit_items_form'])
        else:
            self.moduls['new_items_form'].update_data()
            self.moduls['edit_items_form'].update_data()
        self.show_page(self.ui.btn_new_items, self.ui.items_form)

    def show_product_price_editor_page(self):
        if self.moduls['price_editor_form'] is None:
            self.moduls['price_editor_form'] = PriceEditor(self)
            self.ui.setup_price_editor(self.moduls['price_editor_form'])
        else:
            self.moduls['price_editor_form'].update_data()
        self.show_page(self.ui.btn_price_editor, self.ui.price_editor_form)

    def show_sale_registration_page(self):
        if self.moduls['sale_form'] is None:
            self.moduls['sale_form'] = SaleForm(self)
            self.ui.setup_sale_module(self.moduls['sale_form'])
        else:
            self.moduls['sale_form'].update_data()
        self.show_page(self.ui.btn_sale, self.ui.page_sale_form)

    def show_sellers_places_page(self):
        if self.moduls['sellers_form'] is None and self.moduls['places_form'] is None:
            self.moduls['sellers_form'] = SellersEditor(self)
            self.moduls['places_form'] = PlacesEditor(self)
            self.ui.setup_sellers_and_places_module(self.moduls['sellers_form'], self.moduls['places_form'])
        else:
            self.moduls['sellers_form'].update_data()
            self.moduls['places_form'].update_data()
        self.show_page(self.ui.btn_sellers, self.ui.sellers_and_places_form)

    def show_expenses_page(self):
        if self.moduls['expenses_form'] is None:
            self.moduls['expenses_form'] = ExpensesEditor(self)
            self.ui.setup_expenses_module(self.moduls['expenses_form'])
        else:
            self.moduls['expenses_form'].update_data()
        self.show_page(self.ui.btn_expenses, self.ui.page_expenses_form)

    def show_report_page(self):
        if self.moduls['report_page'] is None:
            self.moduls['report_page'] = ReportPage(self)
            self.ui.setup_report_module(self.moduls['report_page'])
        else:
            self.moduls['report_page'].update_data()
        self.show_page(self.ui.btn_report, self.ui.page_report)

    def show_login_page(self):
        self.show_page(self.ui.login_button, self.ui.page_login_form)

    def show_settings_page_page(self):
        self.show_page(self.ui.settings_button, self.ui.page_settings)

    def on_click_item_sale(self, date: datetime.date):
        self.show_sale_registration_page()
        self.moduls['sale_form'].ui.date_edit.setDate(date)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
