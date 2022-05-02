import re

from prjstore.db.schemas import handler_receiving_the_items as db_schemas
from prjstore.handlers.receiving_the_items_handler import ReceivingTheItemsHandler
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.receiving_the_items.schemas import *
from prjstore.ui.pyside.receiving_the_items.thread import DbConnect, DBSaveData
from prjstore.ui.pyside.receiving_the_items.ui_item import Ui_Dialog
from prjstore.ui.pyside.utils.custom_combo_box import CustomQCompleter
from prjstore.ui.pyside.utils.is_digit import is_digit
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *


class ItemForm(QWidget):
    pd_item: ModelItem
    list_pd_prod: list[ModelProductShow]
    handler: ReceivingTheItemsHandler

    def __init__(self, parent: MainWindowInterface = None, item: ModelItem = ModelItem(), list_pd_product=None,
                 keywords=None, test=False, dark_style=False, user_data=None, db=None):
        super().__init__()
        self.parent: MainWindowInterface = parent
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        if list_pd_product is None:
            list_pd_product = []
        self.list_pd_prod: list[ModelProductShow] = list_pd_product
        self.pd_item: ModelItem = item
        if keywords:
            self.keywords = keywords
        else:
            self.keywords = {'header': 'Получение товара', 'types': (('', 'product'), ('обувь', 'shoes')),
                             'shoes': {'count_sizes': 12, 'min_size': 35,
                                       'header_shoes': ["Размеры", "Количество", "Длина стельки"]}}
        self.test = test
        self.need_update: bool = True
        self.last_added_size = ''
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.dark_style = dark_style
        if self.dark_style:
            self.setup_dark_style()
        self.ui.button_save.clicked.connect(self.on_clicked_button)
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.currentIndexChanged.connect(self.on_name_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.on_edit_name_combo_box)
        self.ui.type_combo_box.currentIndexChanged.connect(self.on_change_product_type)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if parent:
            parent.register_observer(self)
            if parent.dark_style:
                self.setup_dark_style()
            self.__connected_complete(ReceivingTheItemsHandler(main_handler=parent.handler))
        else:
            if not test:
                db_connector = DbConnect(user_data, db)
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
        self.update_ui()

    def setup_ui(self):
        self.setWindowTitle(self.keywords['header'])
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.addItem('')
        self.ui.name_combo_box.setItemData(0, QBrush(QColor("#BDFFB4")), role=Qt.BackgroundRole)
        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)
        for pd_prod in sorted(self.list_pd_prod, key=lambda k: k.id, reverse=True):
            self.ui.name_combo_box.addItem(pd_prod.name, pd_prod)

        self.setup_types()
        # shoes
        self.ui.width_combo_box.clear()
        for width_name, width in self.keywords['shoes']['widths']:
            self.ui.width_combo_box.addItem(width, width_name)
        self.ui.sizes_table.itemChanged.connect(self.on_table_item_edit)

    def update_data(self):
        if self.need_update:
            self.load_widget.show()
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self):
        self.load_widget.show()
        self.list_pd_prod = self.handler.get_products_data()
        self.keywords['shoes']['widths'] = self.handler.get_shoes_widths()
        self.setup_ui()
        self.load_widget.hide()

    def setup_dark_style(self):
        self.setStyleSheet(
            '#Dialog {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            'QLineEdit {background-color: #121212; color: #dcdcdc;}\n'
            '#widget_slis, #widget_items {background-color: #2F303B; border:2px solid #484B5E;  color: #F8F8F2;}'
        )

    def setup_types(self):
        self.ui.type_combo_box.clear()
        for type_text, type_key in self.keywords['types']:
            self.get_type_index(type_key)
            self.ui.type_combo_box.addItem(type_text, type_key)
        self.ui.type_combo_box.setCurrentIndex(1)

    def get_type_index(self, key_name):
        for n, (text, key) in enumerate(self.keywords['types']):
            if key_name == key:
                return n

    def on_edit_name_combo_box(self, text: str):
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

    def show_all_colors(self):
        colors = set()
        unics_colors = list(set(colors))
        self.ui.color_combo_box.clear()
        self.ui.color_combo_box.addItem('')
        for color in unics_colors:
            if color:
                self.ui.color_combo_box.addItem(color)

    def set_enabled_product_fields(self, flag: bool):
        self.ui.price_line_edit.setEnabled(flag)
        self.ui.type_combo_box.setEnabled(flag)

    def on_clicked_button(self):
        if data := self.get_data():
            if not self.test:
                self.load_widget.show()
                db_save_data = DBSaveData(self.handler, data)
                db_save_data.signals.error.connect(self.__connection_error)
                db_save_data.signals.complete.connect(self.__completed_save)
                self.thread_pool.start(db_save_data)

    def __completed_save(self):
        self.update_ui()
        if self.parent:
            self.parent.on_receiving_data_change(self)
        self.load_widget.hide()

    def on_name_combo_box_changed(self):
        self.update_product(self.ui.name_combo_box.currentData())

    def update_product(self, pd_product: Optional[ModelProductShow] = None):
        self.ui.qty_spin_box.setValue(1)
        if pd_product:
            self.ui.price_line_edit.setText(f'{pd_product.price_sell: g}')
            self.ui.type_combo_box.setCurrentIndex(self.get_type_index(key_name=pd_product.type.name))
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
            if color:
                self.ui.color_combo_box.addItem(color)
        # width

        if index := self.ui.width_combo_box.findText(pd_color_shoes.width):
            if index >= 0:
                self.ui.width_combo_box.setCurrentIndex(index)
        # sizes
        self.update_size_table(pd_color_shoes.sizes)

    def update_size_table(self, pd_sizes: Optional[list[ModelSizeShoes]] = None, show_qty=False):
        self.ui.sizes_table.clear()
        self.last_added_size = ''
        self.ui.sizes_table.setHorizontalHeaderLabels(self.keywords['shoes']['header_shoes'])
        count_sizes = self.keywords['shoes']['count_sizes']
        self.ui.sizes_table.setRowCount(count_sizes + 2)
        min_size = self.keywords['shoes']['min_size']
        item = QTableWidgetItem('')
        self.ui.sizes_table.setItem(0, 0, item)
        self.ui.sizes_table.setItem(0, 1, QTableWidgetItem(''))
        self.ui.sizes_table.setItem(0, 2, QTableWidgetItem(''))
        item.setBackground(QColor('#85ff8b'))
        for i, size in enumerate(range(min_size, min_size + count_sizes + 1), start=1):
            self.ui.sizes_table.setItem(i, 0, QTableWidgetItem(f'{size}'))
            self.ui.sizes_table.setItem(i, 1, QTableWidgetItem(''))
            self.ui.sizes_table.setItem(i, 2, QTableWidgetItem(''))
            if pd_sizes and size in pd_sizes:
                if show_qty:
                    self.ui.sizes_table.setItem(i, 1, QTableWidgetItem(f'{pd_sizes[size].qty}'))
                length = pd_sizes[size].length if pd_sizes[size].length else ''
                self.ui.sizes_table.setItem(i, 2, QTableWidgetItem(f'{length}'))
        self.ui.sizes_table.setItemDelegateForColumn(1, LineEditDelegate())

    def on_table_item_edit(self, item):
        if item.row() == 0 and item.column() == 0 and item.text() and item.text() != self.last_added_size:
            self.last_added_size = item.text()
            second_item = self.ui.sizes_table.item(0, 0)
            second_item.setBackground(self.ui.sizes_table.item(2, 0).background())
            self.ui.sizes_table.insertRow(0)
            item = QTableWidgetItem('')
            self.ui.sizes_table.setItem(0, 0, item)
            item.setBackground(QColor('#85ff8b'))
            self.ui.sizes_table.setItem(0, 1, QTableWidgetItem(''))
            self.ui.sizes_table.setItem(0, 2, QTableWidgetItem(''))
        self.ui.sizes_table.sortByColumn(0, Qt.AscendingOrder)

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
        current_data = self.ui.type_combo_box.currentData()
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
        # self.adjustSize()
        self.__hide_qty()

    def get_data(self) -> db_schemas.ModelProduct:
        warning_texts = []
        product_type = self.ui.type_combo_box.currentData()
        product_data = self.ui.name_combo_box.currentData()
        product_id = product_data.id if product_data else None
        product_name = self.ui.name_combo_box.currentText().strip() if self.ui.name_combo_box.currentText() else None
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
            list_of_sizes = []
            for num_row in range(rows):
                size = table.item(num_row, 0).text().replace(',', '.')
                length = None
                if table.item(num_row, 2).text() and is_digit(table.item(num_row, 2).text()):
                    length = table.item(num_row, 2).text()
                qty_shoes = table.item(num_row, 1).text()
                p = re.compile('\d+(\.\d+)?')
                if p.match(size) and qty_shoes.isdigit() and int(qty_shoes) > 0:
                    list_of_sizes.append(db_schemas.ModelSizeShoes(size=size, length=length, qty=qty_shoes))
            if not list_of_sizes:
                warning_texts.append('Не указано количество ниодного размера!')
            pd_shoes = db_schemas.ModelShoes(color=self.ui.color_combo_box.currentText(),
                                             width=self.ui.width_combo_box.currentData(), sizes=list_of_sizes)
        else:
            qty = int(self.ui.qty_spin_box.text())
            if not qty > 0:
                warning_texts.append('Количество должно быть больше нуля!')
        if warning_texts:
            QMessageBox(icon=QMessageBox.Warning, text='\n'.join(warning_texts)).exec()
        else:
            pd_product = db_schemas.ModelProduct(id=product_id, name=product_name, type=product_type,
                                                 price_buy=buy_price,
                                                 price_sell=price_sell, qty=qty, module=pd_shoes)
            return pd_product


class LineEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option: QStyleOptionViewItem, index: QModelIndex, *args, **kwargs) -> QWidget:
        editor = QLineEdit(parent)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        editor.setValidator(validator_reg)
        return editor


if __name__ == "__main__":
    import sys
    from prjstore.db.api import settings

    app = QApplication(sys.argv)
    pd_item = ModelItem()
    w = ItemForm(item=pd_item, test=False, dark_style=True, user_data=settings.user_data)
    w.show()
    sys.exit(app.exec())
