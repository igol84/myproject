import sys

from prjstore.db import API_DB
from prjstore.ui.pyside.login.login_frame import LoginFrame
from prjstore.ui.pyside.main_receiving_the_items import ItemForm
from prjstore.ui.pyside.main_sale_registration import SaleForm
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.main_window.thread import DbConnect
from prjstore.ui.pyside.main_window.ui_main_window import UI_MainWindow
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.push_button import PyPushBottom
from qt_core import *


class MainWindow(QMainWindow, MainWindowInterface):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title')
        self.thread_pool = QThreadPool()
        self.login_form = LoginFrame()
        self.moduls: dict[QWidget] = dict()
        self.moduls['login_form'] = self.login_form
        self.moduls['sale_form'] = QWidget()
        self.moduls['items_form'] = QWidget()
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self, self.moduls)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.show()

        db_connector = DbConnect(self.login_form.get_user_data())
        db_connector.signals.error.connect(self.__connection_error)
        db_connector.signals.result.connect(self.__connected_complete)
        self.thread_pool.start(db_connector)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, db: API_DB):
        self.__db = db
        self.sale_form = SaleForm(parent=self, dark_style=True, db=db)
        self.items_form = ItemForm(parent=self, dark_style=True, db=db)
        self.moduls['sale_form'] = self.sale_form
        self.moduls['items_form'] = self.items_form
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self, self.moduls)
        self.sale_form.setup_dark_style()

        self.ui.btn_1.clicked.connect(self.show_page_1)
        self.ui.btn_2.clicked.connect(self.show_page_2)
        self.ui.login_button.clicked.connect(self.show_page_3)
        self.ui.settings_button.clicked.connect(self.show_page_4)
        self.show_page_2()

        self.load_widget.hide()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if isinstance(btn, PyPushBottom):
                btn.set_active(False)

    def on_update_items(self):
        self.sale_form.update_items_data()

    def show_page_1(self):
        self.reset_selection()
        self.ui.btn_1.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_1)

    def show_page_2(self):
        self.reset_selection()
        self.ui.btn_2.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_2)

    def show_page_3(self):
        self.reset_selection()
        self.ui.login_button.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_3)

    def show_page_4(self):
        self.reset_selection()
        self.ui.settings_button.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
