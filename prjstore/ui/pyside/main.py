import sys

from prjstore.ui.pyside.main_receiving_the_items import ItemForm
from prjstore.ui.pyside.main_sale_registration import SaleForm
from prjstore.ui.pyside.main_window.ui_main_window import UI_MainWindow
from prjstore.ui.pyside.utils.push_button import PyPushBottom
from qt_core import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Title')
        self.sale_form = SaleForm(dark_style=True)
        self.items_form = ItemForm(dark_style=True)
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self, {'sale_form': self.sale_form, 'items_form': self.items_form})
        self.sale_form.setup_dark_style()

        self.ui.btn_1.clicked.connect(self.show_page_1)
        self.ui.btn_2.clicked.connect(self.show_page_2)
        self.ui.settings_button.clicked.connect(self.show_page_3)
        self.show_page_1()
        self.show()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            if isinstance(btn, PyPushBottom):
                btn.set_active(False)

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
        self.ui.settings_button.set_active(True)
        self.ui.pages.setCurrentWidget(self.ui.page_3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
