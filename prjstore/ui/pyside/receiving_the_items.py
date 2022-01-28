from typing import Optional

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QTableWidgetItem, QMessageBox

from prjstore.handlers.receiving_the_items_handler import ReceivingTheItemsHandler
from prjstore.ui.pyside.receiving_the_items.items_ui import Ui_Dialog
from prjstore.ui.pyside.receiving_the_items.schemas import ModelItem, ModelSizeShoes, \
    ModelColorShoesForm, ModelColorShoesShow, ModelProductShow, ModelProductForm
from prjstore.ui.pyside.receiving_the_items.thread import DbConnect
from prjstore.ui.pyside.utils.custom_combo_box import CustomQCompleter
from prjstore.ui.pyside.utils.is_digit import is_digit
from prjstore.ui.pyside.utils.load_widget import LoadWidget


class ItemForm(QWidget):
    pd_item: ModelItem
    list_pd_prod: list[ModelProductShow]
    handler: ReceivingTheItemsHandler

    def __init__(self, item: ModelItem = ModelItem(), list_pd_product=None, keywords=None, test=False):
        super().__init__()
        self.thread_pool = QThreadPool()
        if list_pd_product is None:
            list_pd_product = []
        self.list_pd_prod: list[ModelProductShow] = list_pd_product
        self.pd_item: ModelItem = item
        if keywords:
            self.keywords = keywords
        else:
            self.keywords = {'header': 'Получение товара',
                             'shoes': {'count_sizes': 12, 'min_size': 35, 'widths': ['D', 'EE', '4E'],
                                       'header_shoes': ["Размеры", "Количество", "Длина стельки"]}}
        self.test = test
        self.last_added_size = ''
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.button_save.clicked.connect(self.on_clicked_button)
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.currentIndexChanged.connect(self.on_name_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.on_edit_name_combo_box)
        self.ui.type_combo_box.currentIndexChanged.connect(self.on_change_product_type)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        if not self.test:
            db_connector = DbConnect()
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.__connected_complete)
            self.thread_pool.start(db_connector)
        else:
            self.__connected_complete(ReceivingTheItemsHandler(test=True))

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: ReceivingTheItemsHandler):
        self.handler = handler
        self.list_pd_prod = handler.get_products_data()
        self.setup_ui()
        self.load_widget.hide()

    def setup_ui(self):
        self.setWindowTitle(self.keywords['header'])
        self.ui.name_combo_box.addItem('')
        self.ui.name_combo_box.setItemData(0, QtGui.QBrush(QtGui.QColor("#BDFFB4")), role=QtCore.Qt.BackgroundRole)
        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)
        for pd_prod in self.list_pd_prod:
            self.ui.name_combo_box.addItem(pd_prod.name, pd_prod)
        # shoes
        self.ui.type_combo_box.setCurrentIndex(1)
        self.ui.width_combo_box.clear()
        self.ui.width_combo_box.addItem('')
        for width in self.keywords['shoes']['widths']:
            self.ui.width_combo_box.addItem(width)
        self.setStyleSheet('#sizes_table #first {background-color: #85ff8b;}')
        self.ui.sizes_table.itemChanged.connect(self.on_table_item_edit)

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
        else:
            self.show_all_colors()
            self.ui.type_combo_box.setCurrentIndex(1)

    def show_all_colors(self):
        colors = set()
        for pd_prod in self.list_pd_prod:
            if pd_prod.type.name == 'shoes' and pd_prod.module.colors:
                colors |= pd_prod.module.colors
        unics_colors = list(set(colors))
        self.ui.color_combo_box.clear()
        self.ui.color_combo_box.addItem('')
        for color in unics_colors:
            self.ui.color_combo_box.addItem(color)

    def set_enabled_product_fields(self, flag: bool):
        self.ui.price_line_edit.setEnabled(flag)
        self.ui.type_combo_box.setEnabled(flag)

    def on_clicked_button(self):
        if data := self.get_data():
            self.handler.save_data(data)

    def on_name_combo_box_changed(self):
        self.update_product(self.ui.name_combo_box.currentData())

    def update_product(self, pd_product: Optional[ModelProductShow]):
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
            self.show_all_colors()

    def update_shoes(self, pd_color_shoes: ModelColorShoesShow):
        # color
        self.ui.color_combo_box.clear()
        self.ui.color_combo_box.addItem('')
        for color in pd_color_shoes.colors:
            self.ui.color_combo_box.addItem(color)
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

    def on_table_item_edit(self, item):
        if item.row() == 0 and item.column() == 0 and item.text() and item.text() != self.last_added_size:
            self.last_added_size = item.text()
            second_item = self.ui.sizes_table.item(0, 0)
            second_item.setBackground(self.ui.sizes_table.item(2, 0).background())

            self.ui.sizes_table.insertRow(0)
            item = QTableWidgetItem('')
            self.ui.sizes_table.setItem(0, 0, item)
            item.setBackground(QtGui.QColor('#85ff8b'))
            self.ui.sizes_table.setItem(0, 1, QTableWidgetItem(''))
            self.ui.sizes_table.setItem(0, 2, QTableWidgetItem(''))
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

    def get_data(self) -> ModelProductForm:
        warning_texts = []
        product_type = self.ui.type_combo_box.currentText()
        product_data = self.ui.name_combo_box.currentData()
        product_id = product_data.id if product_data else None
        product_name = self.ui.name_combo_box.currentText() if self.ui.name_combo_box.currentText() else None
        buy_price = self.ui.buy_price_line_edit.text() if is_digit(self.ui.buy_price_line_edit.text()) else None
        price_sell = self.ui.price_line_edit.text() if is_digit(self.ui.price_line_edit.text()) else None
        pd_shoes = None
        qty = None
        if not product_name:
            warning_texts.append('Не указано название продукта!')
        if not price_sell:
            warning_texts.append('Не указана цена продажи!')
        if not buy_price:
            warning_texts.append('Не указана цена покупки!')

        if product_type == 'shoes':
            table = self.ui.sizes_table
            rows = table.rowCount()
            list_of_sizes = {}
            for num_row in range(rows):
                size = table.item(num_row, 0).text()
                length = None
                if table.item(num_row, 2).text() and is_digit(table.item(num_row, 2).text()):
                    length = table.item(num_row, 2).text()
                qty_shoes = table.item(num_row, 1).text()
                if size.isdigit() and qty_shoes.isdigit() and int(qty_shoes) > 0:
                    list_of_sizes[size] = ModelSizeShoes(size=size, length=length, qty=qty_shoes)
            if not list_of_sizes:
                warning_texts.append('Не указано количество ниодного размера!')
            pd_shoes = ModelColorShoesForm(color=self.ui.color_combo_box.currentText(),
                                           width=self.ui.width_combo_box.currentText(), sizes=list_of_sizes)
        else:
            qty = int(self.ui.qty_spin_box.text())
            if not qty > 0:
                warning_texts.append('Количество должно быть больше нуля!')
        if warning_texts:
            QMessageBox(icon=QMessageBox.Warning, text='\n'.join(warning_texts)).exec()
        else:
            pd_product = ModelProductForm(id=product_id, name=product_name, type=product_type, price_buy=buy_price,
                                          price_sell=price_sell, qty=qty, module=pd_shoes)
            return pd_product


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    pd_item = ModelItem()
    w = ItemForm(item=pd_item, test=True)
    w.show()
    sys.exit(app.exec())
