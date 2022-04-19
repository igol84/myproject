import datetime
import sys

from prjstore.db import API_DB
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.main_items_editor import ItemsEditor
from prjstore.ui.pyside.main_login import LoginFrame
from prjstore.ui.pyside.main_places import PlacesEditor
from prjstore.ui.pyside.main_product_price_editor import PriceEditor
from prjstore.ui.pyside.main_receiving_the_items import ItemForm
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

    def __init__(self):
        super().__init__()
        self.moduls: dict[QWidget] = dict()
        self.observers = []
        self.__db = None
        self.handler = None
        self.ui = None
        self.new_items_form: ItemForm = None
        self.edit_items_form: ItemsEditor = None
        self.sale_form: SaleForm = None
        self.sellers_form = None
        self.places_form = None
        self.price_editor_form: PriceEditor = None
        self.thread_pool = QThreadPool()
        self.login_form = LoginFrame(self)
        self.setup_ui()
        self.show()
        self.start_connection()

    def register_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        del self.observers[observer]

    def notify_observer(self, this_observer=None) -> None:
        for observer in self.observers:
            if observer is not this_observer:
                observer.need_update = True

    def data_changed(self, this_observer) -> None:
        self.handler.update_data(this_observer.handler.store)
        self.notify_observer(this_observer)

    def on_receiving_data_change(self, this_observer):
        self.data_changed(this_observer)
        self.edit_items_form.update_data(store=self.handler.store)

    def setup_ui(self, db=None):
        if db:
            self.__db = db
            self.handler = MainHandler(db)
            self.sale_form = SaleForm(self, dark_style=True, db=db)
            self.price_editor_form = PriceEditor(self, dark_style=True, db=db)
            self.new_items_form = ItemForm(self, dark_style=True, db=db)
            self.edit_items_form = ItemsEditor(self, dark_style=True, db=db)
            self.sellers_form = SellersEditor(self, dark_style=True, db=db)
            self.places_form = PlacesEditor(self, dark_style=True, db=db)
            self.sale_form.setup_dark_style()
            self.setWindowTitle(f'Shop - {self.login_form.name}')
        else:
            self.setWindowTitle(f'Shop')
            self.sale_form = QWidget()
            self.price_editor_form = QWidget()
            self.new_items_form = QWidget()
            self.edit_items_form = QWidget()
            self.sellers_form = QWidget()
            self.places_form = QWidget()

        self.moduls['login_form'] = self.login_form
        self.moduls['sale_form'] = self.sale_form
        self.moduls['price_editor_form'] = self.price_editor_form
        self.moduls['new_items_form'] = self.new_items_form
        self.moduls['edit_items_form'] = self.edit_items_form
        self.moduls['sellers_form'] = self.sellers_form
        self.moduls['places_form'] = self.places_form
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self, self.moduls)
        self.ui.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.ui.load_widget.show()

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
        self.setup_ui(db)

        self.ui.btn_new_items.clicked.connect(self.show_items_page)
        self.ui.btn_price_editor.clicked.connect(self.show_product_price_editor_page)
        self.ui.btn_sale.clicked.connect(self.show_sale_registration_page)
        self.ui.btn_sellers.clicked.connect(self.show_sellers_page)
        self.ui.login_button.clicked.connect(self.show_login_page)
        self.ui.settings_button.clicked.connect(self.show_settings_page_page)
        self.show_sale_registration_page()
        self.ui.load_widget.hide()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if isinstance(btn, PyPushBottom):
                btn.set_active(False)

    def show_page(self, btn, form, data_update=True):
        self.reset_selection()
        btn.set_active(True)
        if data_update:
            form.update_data(store=self.handler.store)
        self.ui.pages.setCurrentWidget(form)

    def show_items_page(self):
        self.reset_selection()
        self.ui.btn_new_items.set_active(True)
        self.ui.new_items_form.update_data(store=self.handler.store)
        self.ui.edit_items_form.update_data(store=self.handler.store)
        self.ui.pages.setCurrentWidget(self.ui.items_form)

    def show_product_price_editor_page(self):
        self.show_page(self.ui.btn_price_editor, self.ui.page_product_price_editor)

    def show_sale_registration_page(self):
        self.show_page(self.ui.btn_sale, self.ui.page_sale_form)

    def show_sellers_page(self):
        self.show_page(self.ui.btn_sellers, self.ui.sellers_and_places_form, False)

    def show_login_page(self):
        self.show_page(self.ui.login_button, self.ui.page_login_form, False)

    def show_settings_page_page(self):
        self.show_page(self.ui.settings_button, self.ui.page_settings, False)

    def on_click_item_sale(self, date: datetime.date):
        self.show_sale_registration_page()
        self.sale_form.ui.date_edit.setDate(date)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
