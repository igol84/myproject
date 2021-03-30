import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QDate

from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.qt.qt_utils import clearLayout
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
        self.items = self.handler.store.items

        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        for n, place in enumerate(self.handler.store.places_of_sale):
            self.ui.combo_box_place_of_sale.addItem(place.name, userData=n)
        self.ui.combo_box_seller.addItem('', userData=None)
        for n, seller in enumerate(self.handler.store.sellers):
            self.ui.combo_box_seller.addItem(seller.name, userData=n)

        self._update_sli()

        ItemFrame.parent_form = self
        self.selected_item = None
        self._update_items()

        self.ui.button_hide_sli.clicked.connect(self.on_button_hide_sli)
        self.ui.scroll_items.mousePressEvent = self.on_click_scroll_items
        self.ui.src_items.textChanged.connect(self.on_search_items_by_name)


    def _update_sli(self):
        groupBox = QtWidgets.QGroupBox()
        v_box = QtWidgets.QVBoxLayout(groupBox)
        for i in range(3):
            v_box.addWidget(QtWidgets.QLabel(f"Item{i + 1} qty=1"))
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_box.addItem(spacer)
        self.ui.scroll_slis.setWidget(groupBox)

    def _update_items(self):
        clearLayout(self.ui.items_box)
        self.selected_item = None
        items = self.items
        for key, item in items.items():
            item_frame = ItemFrame(item)
            self.ui.items_box.addWidget(item_frame)
        self.ui.items_box.addStretch(0)

    def on_button_hide_sli(self):
        if self.ui.sale.isHidden():
            self.ui.button_hide_sli.setText('Скрыть')
            self.ui.sale.show()
        else:
            self.ui.button_hide_sli.setText('Отобразить')
            self.ui.sale.hide()

    def on_click_scroll_items(self, e):
        self._update_items()

    def on_search_items_by_name(self):
        src_text = self.ui.src_items.text()
        if src_text:
            self.items = self.handler.search_items(src_text)
            self._update_items()
        else:
            self.items = self.handler.store.items
            self._update_items()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm()
    w.show()
    sys.exit(app.exec_())
