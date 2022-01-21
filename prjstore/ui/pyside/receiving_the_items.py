from typing import Optional

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QTableWidgetItem

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
        self.keywords = {'header': 'Получение товара'}
        self.keywords_shoes = {'count_sizes': 12, 'min_size': 35, 'widths': ['E', 'EE', 'EEE'],
                               'header': ["Размеры", "Количество", "Длина стельки"]}
        self.test = test
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_ui()
        self.update_item()
        self.ui.button_save.clicked.connect(self.on_clicked_button)
        self.ui.name_combo_box.currentIndexChanged.connect(self.on_name_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.on_edit_name_combo_box)
        self.ui.type_combo_box.currentIndexChanged.connect(self.on_edit_product_type)

    def setup_ui(self):
        self.setWindowTitle(self.keywords['header'])
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.addItem('')
        self.ui.name_combo_box.setItemData(0, QtGui.QBrush(QtGui.QColor("#BDFFB4")), role=QtCore.Qt.BackgroundRole)
        for pd_prod in self.list_pd_prod:
            self.ui.name_combo_box.addItem(pd_prod.name, pd_prod)
        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)
        self.ui.width_combo_box.clear()
        self.ui.width_combo_box.addItem('')
        for width in self.keywords_shoes['widths']:
            self.ui.width_combo_box.addItem(width)
        self.update_size_table()

    def on_edit_name_combo_box(self, text):
        if self.ui.name_combo_box.currentIndex() != 0:
            if self.ui.name_combo_box.currentData() and self.ui.name_combo_box.currentData().name != text:
                cursor = self.ui.name_combo_box.lineEdit().cursorPosition()
                self.ui.name_combo_box.setCurrentIndex(0)
                self.ui.name_combo_box.setCurrentText(text)
                self.ui.name_combo_box.lineEdit().setCursorPosition(cursor)

    def on_clicked_button(self):
        print(self.ui.name_combo_box.currentText())
        print(self.ui.name_combo_box.currentData())

    def on_name_combo_box_changed(self):
        self.update_product(self.ui.name_combo_box.currentData())

    def update_product(self, pd_product: Optional[ModelProduct]):
        self.ui.qty_spin_box.setValue(1)
        if pd_product:
            self.ui.price_line_edit.setText(f'{pd_product.price_sell: g}')
            self.ui.type_combo_box.setCurrentText(pd_product.type.name)
            self.on_edit_product_type()
            if pd_product.type.name == 'shoes':
                self.update_shoes(pd_product.shoes)
        else:
            self.ui.price_line_edit.clear()
            self.ui.color_combo_box.setCurrentIndex(0)
            self.ui.width_combo_box.setCurrentIndex(0)
            self.update_size_table()

    def update_shoes(self, pd_color_shoes: ModelColorShoes):
        # color
        self.ui.color_combo_box.clear()
        self.ui.color_combo_box.addItem('')
        colors = {pd_prod.shoes.color for pd_prod in self.list_pd_prod if pd_prod.shoes and pd_prod.shoes.color}
        for color in colors:
            self.ui.color_combo_box.addItem(color)
        self.ui.color_combo_box.setCurrentIndex(self.ui.color_combo_box.findText(pd_color_shoes.color))
        # width
        self.ui.width_combo_box.setCurrentIndex(self.ui.width_combo_box.findText(pd_color_shoes.width))
        # sizes
        self.update_size_table(pd_color_shoes.sizes)

    def update_size_table(self, pd_sizes: Optional[list[ModelSizeShoes]] = None):
        self.ui.sizes_table.clear()
        self.ui.sizes_table.setHorizontalHeaderLabels(self.keywords_shoes['header'])
        count_sizes = self.keywords_shoes['count_sizes']
        min_size = self.keywords_shoes['min_size']
        for i, size in enumerate(range(min_size, min_size + count_sizes + 1)):
            self.ui.sizes_table.setItem(i, 0, QTableWidgetItem(f'{size}'))
            if pd_sizes and size in pd_sizes:
                # self.ui.sizes_table.setItem(i, 1, QTableWidgetItem(f'{pd_sizes[size].qty}'))
                self.ui.sizes_table.setItem(i, 2, QTableWidgetItem(f'{pd_sizes[size].length}'))
        self.ui.sizes_table.setItem(count_sizes, 0, QTableWidgetItem(''))

    def update_item(self):
        if self.pd_item.price_buy:
            self.ui.buy_price_line_edit.setText(f'{self.pd_item.price_buy: g}')
        if self.pd_item.qty:
            self.ui.qty_spin_box.setValue(self.pd_item.qty)
        if self.pd_item.prod_id:
            for pd_product in self.list_pd_prod:
                if pd_product.id == self.pd_item.prod_id:
                    self.ui.name_combo_box.setCurrentIndex(self.ui.name_combo_box.findData(pd_product))
                    self.update_product(pd_product)

    def on_edit_product_type(self):
        current_data = self.ui.type_combo_box.currentText()
        if current_data == 'shoes':
            self.show_shoes()
        else:
            self.hide_shoes()

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
    list_pd_prod = []
    sizes = {38: ModelSizeShoes(size=38, length=24.5, qty=5), 39: ModelSizeShoes(size=39, length=25, qty=8),
             42: ModelSizeShoes(size=42, length=27.5, qty=1), 43: ModelSizeShoes(size=43, length=28, qty=2)}
    shoes = ModelColorShoes(color='black', width='EE', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=115, type='shoes', name='con chak h 70', price_sell=640.40, shoes=shoes))
    list_pd_prod.append(ModelProduct(id=22, type='simple', name='battery', price_sell=840))
    for n in range(23, 24):
        list_pd_prod.append(ModelProduct(id=n, type='simple', name=f'battery {n}', price_sell=840 + n))
    sizes = {36: ModelSizeShoes(size=36, length=23.5, qty=1), 37: ModelSizeShoes(size=37, length=24, qty=2),
             38: ModelSizeShoes(size=38, length=24.5, qty=1), 39: ModelSizeShoes(size=39, length=25, qty=2),
             41: ModelSizeShoes(size=41, length=26.5, qty=3)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 70', price_sell=420, shoes=shoes))

    sizes = {37: ModelSizeShoes(size=37, length=24, qty=1), 38: ModelSizeShoes(size=38, length=24.5, qty=2),
             39: ModelSizeShoes(size=39, length=25, qty=1), 40: ModelSizeShoes(size=40, length=25.5, qty=2)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 75', price_sell=425, shoes=shoes))

    pd_item = ModelItem(id=1, prod_id=115, price_buy=360)
    w = ItemForm(pd_item, list_pd_prod, test=False)
    w.show()
    sys.exit(app.exec())
