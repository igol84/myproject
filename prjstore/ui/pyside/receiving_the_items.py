from PySide6.QtWidgets import QApplication, QWidget, QComboBox

from prjstore.ui.pyside.receiving_the_items.items_ui import Ui_Dialog
from prjstore.ui.pyside.receiving_the_items.schemas import ModelItem, ModelProduct
from prjstore.ui.pyside.utils.custom_combo_box import CustomQCompleter


class ItemForm(QWidget):
    pd_item: ModelItem
    list_pd_item: list[ModelProduct]

    def __init__(self, pd_item: ModelItem = ModelItem(), list_prod=None, test=False):
        super().__init__()
        if list_prod is None:
            list_prod = []
        self.pd_item: ModelItem = pd_item
        self.list_prod: list[ModelProduct] = list_prod
        self.test = test
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.update_ui()
        self.ui.button_save.clicked.connect(self.clicked_button)
        self.ui.name_combo_box.currentIndexChanged.connect(self.name_combo_box_changed)
        self.ui.name_combo_box.currentTextChanged.connect(self.editText)

    def update_ui(self):
        self.ui.name_combo_box.clear()
        self.ui.name_combo_box.addItem('')
        for prod in self.list_prod:
            self.ui.name_combo_box.addItem(prod.name, prod)

        self.ui.name_combo_box.setInsertPolicy(QComboBox.NoInsert)
        completer = CustomQCompleter(self.ui.name_combo_box)
        completer.setModel(self.ui.name_combo_box.model())
        self.ui.name_combo_box.setCompleter(completer)

    def editText(self, text):
        if self.ui.name_combo_box.currentData() and self.ui.name_combo_box.currentData().name != text:
            self.ui.name_combo_box.setCurrentIndex(0)
        self.ui.name_combo_box.setItemText(0, text)

    def clicked_button(self):
        print(self.ui.name_combo_box.currentData())

    def name_combo_box_changed(self, id):
        current_data = self.ui.name_combo_box.currentData()
        if current_data and current_data.type.name == 'shoes':
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
    pr1 = ModelProduct(id=115, type='shoes', name='con chak black 70')
    pr2 = ModelProduct(id=22, type='simple', name='battery')
    pr3 = ModelProduct(id=254, type='shoes', name='con chak red 70')
    list_prod = [pr1, pr2, pr3]
    pd_item = ModelItem(id=1, prod_id=2, qty=5, name='MyName', price=36)
    w = ItemForm(pd_item=pd_item, list_prod=list_prod, test=False)
    w.show()
    sys.exit(app.exec())
