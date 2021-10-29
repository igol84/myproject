import sys

from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QDialogButtonBox, QMessageBox
from PySide2.QtCore import QDate

from prjstore.db import API_DB
from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.pyside.qt_utils import clearLayout
from prjstore.ui.pyside.sale_registration.components import FrameItemFactory
from prjstore.ui.pyside.sale_registration.components.abstract_product import Item
from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.sale_registration_ui import Ui_Form
from prjstore.ui.pyside.sale_registration.schemas import ModelProduct


class SaleForm(QWidget):
    def __init__(self, db=None, test=False):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.resize(1200, 600)
        if not test and db is None:
            db = API_DB()
        self.handler = SaleRegistrationHandler(test=test, db=db)
        self.items: dict[str, ModelProduct] = None
        self.sli_list: dict[tuple[str, float]: ModelProduct] = self.handler.get_sale_line_items()
        self.selected_sli_widget: SLI_Frame = None
        self.selected_item_widget: Item = None

        # SLI ----------------------- left panel ------------------------------
        self.ui.date_edit.setDate(QDate.currentDate())
        self.ui.date_edit.dateChanged.connect(self.on_date_edit_changed)

        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        for i, name_place_of_sale in self.handler.get_store_places_of_sale_names().items():
            self.ui.combo_box_place_of_sale.addItem(name_place_of_sale, userData=i)
        self.ui.combo_box_place_of_sale.currentIndexChanged.connect(self.on_combo_box_place_of_sale_changed)

        self.ui.combo_box_seller.addItem('', userData=None)
        for i, seller_name in self.handler.get_store_sellers_names().items():
            self.ui.combo_box_seller.addItem(seller_name, userData=i)
        self.ui.combo_box_seller.currentIndexChanged.connect(self.on_combo_box_seller_changed)

        self._update_sli()

        # Items -------------------- right panel --------------------------------
        self._update_items_layout()

        self.ui.src_items.textChanged.connect(self.on_search_items_text_changed)

        # Items -------------------- Ok Cancel --------------------------------
        self.save_button = QPushButton('Сохранить')
        self.ui.buttonBox.addButton(self.save_button, QDialogButtonBox.AcceptRole)
        self.ui.buttonBox.accepted.connect(self.press_save)

    def mousePressEvent(self, event):
        self._update_sli()
        self._update_items_layout()

    # SLI ----------------------- left panel ------------------------------
    def _update_sli(self):
        clearLayout(self.ui.sli_layout)
        self.selected_sli_widget = None
        self.sli_list = self.handler.get_sale_line_items()
        for sli in self.sli_list.values():
            label = SLI_Frame(self, sli.prod_id, sli.name, sli.price, sli.price_format, sli.qty)
            self.ui.sli_layout.addWidget(label)
        self.ui.sli_layout.addStretch(0)

    def _update_total(self):
        self.ui.total.setText(self.handler.get_total())

    def on_date_edit_changed(self, date: QDate):
        # self.handler.change_date(date.toPython())
        pass

    def on_combo_box_place_of_sale_changed(self, combo_box_place_of_sale_id):
        pass

    def on_combo_box_seller_changed(self, combo_box_seller_id):
        pass

    # Items -------------------- right panel --------------------------------
    def _update_items_layout(self):
        clearLayout(self.ui.items_layout)
        self.selected_item_widget = None
        self.items = self.handler.get_store_items(search=self.ui.src_items.text())
        for item in self.items:
            item_frame = FrameItemFactory.create(product_type=item.type, parent=self, item_pd=item)
            self.ui.items_layout.addWidget(item_frame)
        self.ui.items_layout.addStretch(0)

    def on_click_scroll_items(self, event):
        if event:
            pass
        self._update_items_layout()

    def on_search_items_text_changed(self):
        self._update_items_layout()

    def put_on_sale(self):
        pr_id = self.selected_item_widget.pr_id
        sale_price = self.selected_item_widget.get_sale_price()
        sale_qty = self.selected_item_widget.get_sale_qty()
        self.handler.put_on_sale(pr_id, int(sale_qty), float(sale_price))

        if self.handler.is_item_exists(pr_id):
            self.selected_item_widget.pr_qty = self.handler.get_item_qty_by_product_id(pr_id)
        else:
            if self.ui.src_items.text():
                del self.items[pr_id]
            self._update_items_layout()
        self._update_sli()
        self._update_total()
        self.ui.src_items.clear()

    def put_item_form_sli_to_items(self):
        sli_id = self.selected_sli_widget.sli_product_id
        sli_price = self.selected_sli_widget.sli_price
        self.handler.put_item_form_sli_to_items(sli_id, sli_price)
        self._update_sli()
        self._update_items_layout()
        self._update_total()

    def edit_sale_price_in_sli(self, sli_item_id: str, old_sale_price: float, sale_price: float):
        self.handler.edit_sale_price_in_sli(sli_item_id, old_sale_price, sale_price)
        self._update_sli()
        self._update_total()

    def press_save(self):
        current_data = self.ui.date_edit.date().toPython()
        current_place_of_sale_id = self.ui.combo_box_place_of_sale.currentData()
        current_seller_id = self.ui.combo_box_seller.currentData()
        if self.handler.end_sale(current_data, current_place_of_sale_id, current_seller_id):
            QMessageBox(icon=QMessageBox.Information, text='Продажа выполнена!').exec_()
            self.close()
        else:
            warning_texts = []
            if not self.ui.combo_box_place_of_sale.currentText():
                warning_texts.append('Не вабрано место продажи!')
            if not self.ui.combo_box_seller.currentText():
                warning_texts.append('Не вабран продавец!')
            if not self.sli_list:
                warning_texts.append('Нет товаров в списке продаж!')
            QMessageBox(icon=QMessageBox.Warning, text='\n'.join(warning_texts)).exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm(test=True)
    w.show()
    sys.exit(app.exec_())
