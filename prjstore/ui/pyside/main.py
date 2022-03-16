import sys

from prjstore.db import API_DB
from prjstore.ui.pyside.main_login import LoginFrame
from prjstore.ui.pyside.main_product_price_editor import PriceEditor
from prjstore.ui.pyside.main_receiving_the_items import ItemForm
from prjstore.ui.pyside.main_sale_registration import SaleForm
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.main_window.thread import DbConnect
from prjstore.ui.pyside.main_window.ui_main_window import UI_MainWindow
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.push_button import PyPushBottom
from prjstore.ui.pyside.utils.qt_core import *


class MainWindow(QMainWindow, MainWindowInterface):
    def __init__(self):
        super().__init__()
        self.__db = None
        self.ui = None
        self.items_form: ItemForm = None
        self.sale_form: SaleForm = None
        self.price_editor_form: PriceEditor = None
        self.setWindowTitle('Title')
        self.thread_pool = QThreadPool()
        self.login_form = LoginFrame(self)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.load_widget.show()
        self.setup_ui()
        self.show()
        self.start_connection()

    def setup_ui(self, db=None):
        if db:
            self.__db = db
            self.sale_form = SaleForm(self, dark_style=True, db=db)
            self.price_editor_form = PriceEditor(self, dark_style=True, db=db)
            self.items_form = ItemForm(self, dark_style=True, db=db)
            self.sale_form.setup_dark_style()
        else:
            self.sale_form = QWidget()
            self.price_editor_form = QWidget()
            self.items_form = QWidget()

        moduls: dict[QWidget] = dict()
        moduls['login_form'] = self.login_form
        moduls['sale_form'] = self.sale_form
        moduls['price_editor_form'] = self.price_editor_form
        moduls['items_form'] = self.items_form
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self, moduls)

    def start_connection(self):
        db_connector = DbConnect(self.login_form.get_user_data())
        db_connector.signals.connection_error.connect(self.__connection_error)
        db_connector.signals.authentication_error.connect(self.__authentication_error)
        db_connector.signals.result.connect(self.__connected_complete)
        self.thread_pool.start(db_connector)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __authentication_error(self, err: str):
        self.setup_ui()
        self.show_login_page()
        self.load_widget.hide()
        QMessageBox.warning(self, err, err)

    def __connected_complete(self, db: API_DB):
        self.setup_ui(db)

        self.ui.btn_new_items.clicked.connect(self.show_receiving_the_items_page)
        self.ui.btn_price_editor.clicked.connect(self.show_product_price_editor_page)
        self.ui.btn_sale.clicked.connect(self.show_sale_registration_page)
        self.ui.login_button.clicked.connect(self.show_login_page)
        self.ui.settings_button.clicked.connect(self.show_settings_page_page)
        self.show_sale_registration_page()

        self.load_widget.hide()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if isinstance(btn, PyPushBottom):
                btn.set_active(False)

    def show_product_price_editor_page(self):
        self.reset_selection()
        self.ui.btn_price_editor.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_product_price_editor)

    def show_receiving_the_items_page(self):
        self.reset_selection()
        self.ui.btn_new_items.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_items_form)

    def show_sale_registration_page(self):
        self.reset_selection()
        self.ui.btn_sale.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_sale_form)

    def show_login_page(self):
        self.reset_selection()
        self.ui.login_button.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_login_form)

    def show_settings_page_page(self):
        self.reset_selection()
        self.ui.settings_button.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_settings)

    # -------------------on update pages-------------------------

    def on_update_receiving_items(self):
        self.sale_form.update_items_data()
        self.price_editor_form.update_data()

    def on_update_product_price_editor(self):
        self.sale_form.update_items_data()
        self.items_form.update_data()

    def on_update_sale_registration(self):
        self.price_editor_form.update_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
