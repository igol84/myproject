from typing import Optional

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QTableWidgetItem

from prjstore.ui.pyside.receiving_the_items.items_ui import Ui_Dialog
from prjstore.ui.pyside.receiving_the_items.schemas import ModelItem, ModelProduct, ModelColorShoes, ModelSizeShoes
from prjstore.ui.pyside.utils.custom_combo_box import CustomQCompleter
from prjstore.ui.pyside.utils.is_digit import is_digit


class ItemForm(QWidget):
    pd_item: ModelItem
    list_pd_prod: list[ModelProduct]

    def __init__(self, item: ModelItem = ModelItem(), list_pd_product=None, keywords=None, test=False):
        super().__init__()
        if list_pd_product is None:
            list_pd_product = []
        self.pd_item: ModelItem = item
        self.list_pd_prod: list[ModelProduct] = list_pd_product
        if keywords:
            self.keywords = keywords
        else:
            self.keywords = {'header': 'Получение товара',
                             'shoes': {'count_sizes': 12, 'min_size': 35, 'widths': ['E', 'EE', 'EEE'],
                                       'header_shoes': ["Размеры", "Количество", "Длина стельки"]}}
        self.test = test
        self.last_added_size = ''
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_ui()
        self.update_item()
        self.ui.button_save.clicked.connect(self.on_clicked_button)
        self.ui.name_combo_box.currentIndexChanged.connect(self.on_name_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.on_edit_name_combo_box)
        self.ui.type_combo_box.currentIndexChanged.connect(self.on_change_product_type)

    def setup_ui(self):
        self.setWindowTitle(self.keywords['header'])
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.addItem('')
        self.ui.name_combo_box.setItemData(0, QtGui.QBrush(QtGui.QColor("#BDFFB4")), role=QtCore.Qt.BackgroundRole)
        for pd_prod in self.list_pd_prod:
            self.ui.name_combo_box.addItem(pd_prod.name, pd_prod)
            self.set_enabled_product_fields(False)
        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)
        # shoes
        self.ui.width_combo_box.clear()
        self.ui.width_combo_box.addItem('')
        for width in self.keywords['shoes']['widths']:
            self.ui.width_combo_box.addItem(width)

        self.setStyleSheet('#sizes_table #first {background-color: #85ff8b;}')
        self.ui.sizes_table.itemChanged.connect(self.calculadora)

    def on_edit_name_combo_box(self, text):
        self.set_enabled_product_fields(True)
        if self.ui.name_combo_box.currentIndex() != 0:
            if self.ui.name_combo_box.currentData() and self.ui.name_combo_box.currentData().name != text:
                cursor = self.ui.name_combo_box.lineEdit().cursorPosition()
                self.ui.name_combo_box.setCurrentIndex(0)
                self.ui.name_combo_box.setCurrentText(text)
                self.ui.name_combo_box.lineEdit().setCursorPosition(cursor)
            else:
                self.set_enabled_product_fields(False)

    def set_enabled_product_fields(self, flag: bool):
        self.ui.price_line_edit.setEnabled(flag)
        self.ui.type_combo_box.setEnabled(flag)

    def on_clicked_button(self):
        print(self.export_data())

    def export_data(self):
        product_type = self.ui.type_combo_box.currentText()
        pd_shoes = None
        qty = None
        if product_type == 'shoes':
            table = self.ui.sizes_table
            rows = table.rowCount()
            list_of_sizes = {}
            for num_row in range(rows):
                size = table.item(num_row, 0).text()
                length = table.item(num_row, 2).text() if is_digit(table.item(num_row, 2).text()) else None
                qty_shoes = table.item(num_row, 1).text()
                if size.isdigit() and qty_shoes.isdigit() and int(qty_shoes) > 0:
                    list_of_sizes[size] = ModelSizeShoes(size=size, length=length, qty=qty_shoes)
            pd_shoes = ModelColorShoes(color=self.ui.color_combo_box.currentText(),
                                       width=self.ui.width_combo_box.currentText(), sizes=list_of_sizes)
        else:
            qty = self.ui.qty_spin_box.text()
        pd_prod = ModelProduct(type=product_type, price_buy=self.ui.buy_price_line_edit.text(),
                               price_sell=self.ui.price_line_edit.text(), qty=qty,
                               module=pd_shoes, name=self.ui.name_combo_box.currentText())
        return pd_prod

    def on_name_combo_box_changed(self):
        self.update_product(self.ui.name_combo_box.currentData())

    def update_product(self, pd_product: Optional[ModelProduct]):
        self.ui.qty_spin_box.setValue(1)
        if pd_product:
            self.ui.price_line_edit.setText(f'{pd_product.price_sell: g}')
            self.ui.type_combo_box.setCurrentText(pd_product.type.name)
            self.on_change_product_type()
            if pd_product.type.name == 'shoes':
                self.update_shoes(pd_product.module)
        else:
            self.ui.price_line_edit.clear()
            self.ui.color_combo_box.setCurrentIndex(0)
            self.ui.width_combo_box.setCurrentIndex(0)
            self.update_size_table()

    def update_shoes(self, pd_color_shoes: ModelColorShoes):
        # color
        self.ui.color_combo_box.clear()
        colors = {pd_prod.module.color for pd_prod in self.list_pd_prod if pd_prod.module and pd_prod.module.color}
        for color in colors:
            self.ui.color_combo_box.addItem(color)
        self.ui.color_combo_box.setCurrentIndex(self.ui.color_combo_box.findText(pd_color_shoes.color))
        # width
        self.ui.width_combo_box.setCurrentIndex(self.ui.width_combo_box.findText(pd_color_shoes.width))
        # sizes
        self.update_size_table(pd_color_shoes.sizes)

    def update_size_table(self, pd_sizes: Optional[list[ModelSizeShoes]] = None, show_qty=False):
        self.ui.sizes_table.clear()
        self.ui.sizes_table.setHorizontalHeaderLabels(self.keywords['shoes']['header_shoes'])
        count_sizes = self.keywords['shoes']['count_sizes']
        min_size = self.keywords['shoes']['min_size']
        item = QTableWidgetItem('')
        self.ui.sizes_table.setItem(0, 0, item)
        self.ui.sizes_table.setItem(0, 1, QTableWidgetItem(''))
        self.ui.sizes_table.setItem(0, 2, QTableWidgetItem(''))
        item.setBackground(QtGui.QColor('#85ff8b'))
        for i, size in enumerate(range(min_size, min_size + count_sizes + 1), start=1):
            self.ui.sizes_table.setItem(i, 0, QTableWidgetItem(f'{size}'))
            self.ui.sizes_table.setItem(i, 1, QTableWidgetItem())
            self.ui.sizes_table.setItem(i, 2, QTableWidgetItem())
            if pd_sizes and size in pd_sizes:
                if show_qty:
                    self.ui.sizes_table.setItem(i, 1, QTableWidgetItem(f'{pd_sizes[size].qty}'))
                self.ui.sizes_table.setItem(i, 2, QTableWidgetItem(f'{pd_sizes[size].length}'))

    def calculadora(self, item):
        if item.row() == 0 and item.column() == 0 and item.text() and item.text() != self.last_added_size:
            self.last_added_size = item.text()
            second_item = self.ui.sizes_table.item(0, 0)
            second_item.setBackground(self.ui.sizes_table.item(2, 0).background())

            self.ui.sizes_table.insertRow(0)
            item = QTableWidgetItem('')
            self.ui.sizes_table.setItem(0, 0, item)
            item.setBackground(QtGui.QColor('#85ff8b'))
            self.ui.sizes_table.setItem(0, 1, QTableWidgetItem(''))
        self.ui.sizes_table.sortByColumn(0, QtCore.Qt.AscendingOrder)

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

    def on_change_product_type(self):
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
    list_pd_prod.append(ModelProduct(id=115, type='shoes', name='con chak h 70', price_sell=640.40, module=shoes))
    list_pd_prod.append(ModelProduct(id=22, type='simple', name='battery', price_sell=840))
    for n in range(23, 24):
        list_pd_prod.append(ModelProduct(id=n, type='simple', name=f'battery {n}', price_sell=840 + n))
    sizes = {36: ModelSizeShoes(size=36, length=23.5, qty=1), 37: ModelSizeShoes(size=37, length=24, qty=2),
             38: ModelSizeShoes(size=38, length=24.5, qty=1), 39: ModelSizeShoes(size=39, length=25, qty=2),
             41: ModelSizeShoes(size=41, length=26.5, qty=3)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 70', price_sell=420, module=shoes))

    sizes = {37: ModelSizeShoes(size=37, length=24, qty=1), 38: ModelSizeShoes(size=38, length=24.5, qty=2),
             39: ModelSizeShoes(size=39, length=25, qty=1), 40: ModelSizeShoes(size=40, length=25.5, qty=2)}
    shoes = ModelColorShoes(color='white', sizes=sizes)
    list_pd_prod.append(ModelProduct(id=254, type='shoes', name='con chak l 75', price_sell=425, module=shoes))

    pd_item = ModelItem(id=1, prod_id=115, price_buy=360)
    w = ItemForm(pd_item, list_pd_prod, test=False)
    w.show()
    sys.exit(app.exec())
