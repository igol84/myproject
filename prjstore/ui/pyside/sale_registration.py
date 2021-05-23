import sys

from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtCore import QDate

from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.pyside.qt_utils import clearLayout
from prjstore.ui.pyside.sale_registration_components.sale_registration_product import ItemFrame
from prjstore.ui.pyside.sale_registration_ui import Ui_Form


class SaleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.resize(1200, 600)
        self.handler = SaleRegistrationHandler()
        self.handler.test()
        self.items = self.handler.store.items
        self.selected_item_widget: ItemFrame = None

        # SLI ----------------------- left panel ------------------------------
        self.ui.date_edit.setDate(QDate.currentDate())
        self.ui.date_edit.dateChanged.connect(self.on_date_edit_changed)
        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        for n, place in enumerate(self.handler.store.places_of_sale):
            self.ui.combo_box_place_of_sale.addItem(place.name, userData=n)
        self.ui.combo_box_place_of_sale.currentIndexChanged.connect(self.on_combo_box_place_of_sale_changed)
        self.ui.combo_box_seller.addItem('', userData=None)
        for n, seller in enumerate(self.handler.store.sellers):
            self.ui.combo_box_seller.addItem(seller.name, userData=n)
        self.ui.combo_box_seller.currentIndexChanged.connect(self.on_combo_box_seller_changed)

        self._update_sli()
        self.ui.button_hide_sli.clicked.connect(self.on_button_hide_sli)

        # Items -------------------- right panel --------------------------------
        self._update_items_layout()

        self.ui.scroll_items.mousePressEvent = self.on_click_scroll_items
        self.ui.src_items.textChanged.connect(self.on_search_items)

    # SLI ----------------------- left panel ------------------------------
    def _update_sli(self):
        clearLayout(self.ui.sli_layout)

    def on_button_hide_sli(self):
        if self.ui.sale.isHidden():
            self.ui.button_hide_sli.setText('Скрыть')
            self.ui.sale.show()
        else:
            self.ui.button_hide_sli.setText('Отобразить')
            self.ui.sale.hide()

    def on_date_edit_changed(self, date: QDate):
        print(date.toString('dd.MM.yyyy'))
        self._update_sli()

    def on_combo_box_place_of_sale_changed(self, combo_box_place_of_sale_id):
        place_of_sale_id = self.ui.combo_box_place_of_sale.itemData(combo_box_place_of_sale_id)
        if place_of_sale_id is not None:
            print(self.handler.store.places_of_sale[place_of_sale_id])
        self._update_sli()

    def on_combo_box_seller_changed(self, combo_box_seller_id):
        seller_id = self.ui.combo_box_seller.itemData(combo_box_seller_id)
        if seller_id is not None:
            print(self.handler.store.sellers[seller_id])
        self._update_sli()

    # Items -------------------- right panel --------------------------------
    def _update_items_layout(self):
        clearLayout(self.ui.items_layout)
        self.selected_item_widget = None
        for key, item in self.items.items():
            item_frame = ItemFrame(self, item)
            self.ui.items_layout.addWidget(item_frame)
        self.ui.items_layout.addStretch(0)

    def on_click_scroll_items(self, event):
        self._update_items_layout()

    def on_search_items(self):
        src_text = self.ui.src_items.text()
        if src_text:
            self.items = self.handler.search_items(src_text)
            self._update_items_layout()
        else:
            self.items = self.handler.store.items
            self._update_items_layout()

    def put_on_sale(self):
        item = self.selected_item_widget.item
        sale_price = self.selected_item_widget.price_line_edit.text()
        qty = self.selected_item_widget.count_box.text()
        self.handler.put_on_sale(item, int(qty), float(sale_price))
        for line in self.handler.sale.line_items:
            print(line)
        print()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm()
    w.show()
    sys.exit(app.exec_())
