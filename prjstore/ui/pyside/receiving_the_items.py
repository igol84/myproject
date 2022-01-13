from PySide6.QtWidgets import QApplication, QWidget

from prjstore.ui.pyside.receiving_the_items.items_ui import Ui_Dialog
from prjstore.ui.pyside.receiving_the_items.schemas import ModelItem


class ItemForm(QWidget):

    def __init__(self, pd_item: ModelItem, test=False):
        super().__init__()
        self.pd_item = pd_item
        self.test = test
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.hide_shoes()
        self.ui.button_save.clicked.connect(self.clicked_button)
        self.ui.name_combo_box.editTextChanged.connect(self.findText)

    def findText(self, s):
        print(s)
        index=self.ui.name_combo_box.findText(s)
        if index > -1:
            self.ui.name_combo_box.setCurrentIndex(index)

    def clicked_button(self):
        if self.ui.sizes_table.isHidden():
            self.show_shoes()
        else:
            self.hide_shoes()

    def hide_qty(self):
        if not self.ui.qty_label.isHidden():
            self.ui.qty_label.hide()
            self.ui.qty_spin_box.hide()
            self.resize(self.size())

    def show_qty(self):
        if self.ui.qty_label.isHidden():
            self.ui.qty_label.show()
            self.ui.qty_spin_box.show()

    def hide_shoes(self):
        if not self.ui.sizes_table.isHidden():
            self.ui.color_label.hide()
            self.ui.color_combo_box.hide()
            self.ui.width_label.hide()
            self.ui.width_combo_box.hide()
            self.ui.sizes_table.hide()
            self.show_qty()
            self.resize(self.size().width(), 170)

    def show_shoes(self):
        if self.ui.sizes_table.isHidden():
            self.ui.color_label.show()
            self.ui.color_combo_box.show()
            self.ui.width_label.show()
            self.ui.width_combo_box.show()
            self.ui.sizes_table.show()
            self.hide_qty()
            self.resize(self.size().width(), 500)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    pd_item = ModelItem(type='shoes')
    w = ItemForm(pd_item=pd_item, test=False)
    w.show()
    sys.exit(app.exec())
