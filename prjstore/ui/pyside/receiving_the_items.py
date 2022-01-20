from typing import Optional

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QComboBox

from prjstore.ui.pyside.receiving_the_items.items_ui import Ui_Dialog
from prjstore.ui.pyside.receiving_the_items.schemas import ModelItem, ModelProduct, ModelColorShoes, ModelSizeShoes
from prjstore.ui.pyside.utils.custom_combo_box import CustomQCompleter


class ItemForm(QWidget):
    pd_item: ModelItem
    list_pd_prod: list[ModelProduct]

    def __init__(self, item: ModelItem = ModelItem(), list_pd_product=None, test=False):
        super().__init__()
        if list_pd_product is None:
            list_pd_product = []
        self.pd_item: ModelItem = item
        self.list_pd_prod: list[ModelProduct] = list_pd_product
        self.test = test
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.update_ui()
        self.update_item()
        self.ui.button_save.clicked.connect(self.on_clicked_button)
        self.ui.name_combo_box.currentIndexChanged.connect(self.on_name_combo_box_changed)
        self.ui.type_combo_box.currentIndexChanged.connect(self.on_type_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.on_edit_name_combo_box)

    def update_ui(self):
        self.on_name_combo_box_changed()
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.addItem('')
        self.ui.name_combo_box.setItemData(0, QtGui.QBrush(QtGui.QColor("#BDFFB4")), role=QtCore.Qt.BackgroundRole)
        for prod in self.list_pd_prod:
            self.ui.name_combo_box.addItem(prod.name, prod)
        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)

    def on_edit_name_combo_box(self, text):
        if self.ui.name_combo_box.currentIndex() != 0:
            if self.ui.name_combo_box.currentData() and self.ui.name_combo_box.currentData().name != text:
                self.ui.name_combo_box.setCurrentIndex(0)
            self.ui.name_combo_box.setCurrentText(text)

    def on_clicked_button(self):
        print(self.ui.name_combo_box.currentText())
        print(self.ui.name_combo_box.currentData())

    def on_name_combo_box_changed(self, selected_id=None):
        self.update_product(self.ui.name_combo_box.currentData())
        return selected_id

    def update_product(self, pd_product: Optional[ModelProduct]):
        if pd_product:
            self.ui.price_line_edit.setText(f'{pd_product.price_sell: g}')
            self.ui.type_combo_box.setCurrentText(pd_product.type.name)
            if pd_product.type.name == 'shoes':
                self.show_shoes()
            else:
                self.hide_shoes()
        else:
            self.ui.price_line_edit.clear()
            self.ui.type_combo_box.setCurrentIndex(0)

    def update_item(self):
        if self.pd_item.price_buy:
            self.ui.buy_price_line_edit.setText(f'{self.pd_item.price_buy: g}')
        if self.pd_item.qty:
            self.ui.qty_spin_box.setValue(self.pd_item.qty)
        if self.pd_item.prod_id:
            for pd_product in self.list_pd_prod:
                if pd_product.id == self.pd_item.prod_id:
                    self.ui.name_combo_box.setCurrentText(pd_product.name)
                    self.update_product(pd_product)

    def on_type_combo_box_changed(self, selected_id):
        current_data = self.ui.type_combo_box.currentText()
        if current_data == 'shoes':
            self.show_shoes()
        else:
            self.hide_shoes()
        return selected_id

    def __hide_qty(self):
        if not self.ui.qty_label.isHidden():
            self.ui.qty_label.hide()
            self.ui.qty_spin_box.hide()

    def __show_qty(self):
        if self.ui.qty_label.isHidden():
            self.ui.qty_label.show()
            self.ui.qty_spin_box.show()

    def hide_shoes(self):
        for i in range(self.ui.sizes_grid.count() - 1, -1, -1):
            x = self.ui.sizes_grid.itemAt(i).widget()
            x.hide()
        self.ui.sizes_grid.activate()
        self.adjustSize()
        self.__show_qty()

    def show_shoes(self):
        for i in range(self.ui.sizes_grid.count() - 1, -1, -1):
            x = self.ui.sizes_grid.itemAt(i).widget()
            x.show()
        self.ui.sizes_grid.activate()
        self.adjustSize()
        self.__hide_qty()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    sizes = [ModelSizeShoes(size=38, length=24.5, qty=5), ModelSizeShoes(size=39, length=25, qty=8),
             ModelSizeShoes(size=42, length=27.5, qty=1), ModelSizeShoes(size=43, length=28, qty=2)]
    shoes = ModelColorShoes(color='black', width='EE', sizes=sizes)
    pr1 = ModelProduct(id=115, type='shoes', name='con chak h 70', price_sell=640.40, shoes=shoes)
    pr2 = ModelProduct(id=22, type='simple', name='battery', price_sell=840)
    sizes = [ModelSizeShoes(size=36, length=23.5, qty=1), ModelSizeShoes(size=37, length=24, qty=2),
             ModelSizeShoes(size=38, length=24.5, qty=1), ModelSizeShoes(size=39, length=25, qty=2)]
    shoes = ModelColorShoes(color='black', sizes=sizes)
    pr3 = ModelProduct(id=254, type='shoes', name='con chak l 70', price_sell=420, shoes=shoes)
    list_pd_prod = [pr1, pr2, pr3]

    pd_item = ModelItem(id=1, prod_id=115, price_buy=360)
    w = ItemForm(pd_item, list_pd_prod, test=False)
    w.show()
    sys.exit(app.exec())
