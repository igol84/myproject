import sys

from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy
from PyQt5.QtCore import QDate

from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.qt.sale_registration_ui import *


class SaleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.handler = SaleRegistrationHandler()
        self.handler.test()

        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        for n, place in enumerate(self.handler.store.places_of_sale):
            self.ui.combo_box_place_of_sale.addItem(place.name, userData=n)
        self.ui.combo_box_seller.addItem('', userData=None)
        for n, seller in enumerate(self.handler.store.sellers):
            self.ui.combo_box_seller.addItem(seller.name, userData=n)

        v_box = QtWidgets.QVBoxLayout()
        self.items = [f"Item{i+1}" for i in range(8)]
        for item in self.items:
            v_box.addWidget(QtWidgets.QLabel(item))
        v_box.addStretch(0)
        self.ui.scroll_items.setLayout(v_box)

        groupBox = QtWidgets.QGroupBox()
        v_box = QtWidgets.QVBoxLayout(groupBox)
        for i in range(3):
            v_box.addWidget(QtWidgets.QLabel(f"Item{i+1} qty=1"))
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_box.addItem(spacer)
        self.ui.scroll_slis.setWidget(groupBox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm()
    w.show()
    sys.exit(app.exec_())