import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QDate

from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.qt.sale_registration_components.sale_registration_product import ItemFrame
from prjstore.ui.qt.sale_registration_ui import *


class SaleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.resize(1200, 600)
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

        ItemFrame.sale_form = self
        self._update_sli()
        self._update_items()


    def _update_sli(self):
        groupBox = QtWidgets.QGroupBox()
        v_box = QtWidgets.QVBoxLayout(groupBox)
        for i in range(3):
            v_box.addWidget(QtWidgets.QLabel(f"Item{i + 1} qty=1"))
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_box.addItem(spacer)
        self.ui.scroll_slis.setWidget(groupBox)

    def _update_items(self):
        self.items_box = QtWidgets.QVBoxLayout()
        items = self.handler.store.items
        for key, item in items.items():
            item_frame = ItemFrame(item)
            self.items_box.addWidget(item_frame)
        self.items_box.addStretch(0)
        self.ui.scroll_items.setLayout(self.items_box)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm()
    w.show()
    sys.exit(app.exec_())
