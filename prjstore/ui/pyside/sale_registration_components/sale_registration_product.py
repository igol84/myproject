import sys

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QFontMetrics
from PySide2.QtWidgets import QWidget, QApplication, QSpinBox, QPushButton


class ItemFrame(QWidget):
    __color_fon = '#E1E1E1'
    __h = 30
    __w = 300

    def __init__(self, parent, pr_item):
        super().__init__()
        self.__parent_form = parent
        self.item = pr_item
        self.setMinimumSize(self.__w, self.__h)
        self.setToolTip(self.item.product.name)
        self.setToolTipDuration(2000)
        self.count_box = QSpinBox(self)
        self.count_box.setRange(1, self.item.qty)
        self.btn_plus = QPushButton(parent=self, text='+')
        self.btn_plus.setMaximumSize(25, 25)
        self.btn_plus.clicked.connect(self.on_push_button)

        self.count_box.setRange(1, self.item.qty)

        self.count_box.hide()
        self.btn_plus.hide()

    def get_parent_form(self):
        return self.__parent_form

    parent_form = property(get_parent_form)

    def sizeHint(self):
        return QtCore.QSize(self.__w, self.__h)

    def paintEvent(self, e):
        self.count_box.move(self.width() - self.count_box.width() - 3 - self.btn_plus.width() - 3, 4)
        self.btn_plus.move(self.width() - self.btn_plus.width() - 3, 3)
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.__color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('#555'))
        painter.setPen(pen)
        painter.drawRect(-1, -1, painter.device().width() - 1, painter.device().height() - 1)

        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)
        fm = QFontMetrics(font)
        text_item_name = f'{self.item.product.id}:{self.item.product.name}'
        text_item_price = f'{self.item.product.price.format_my()}'
        text_item_qty = f'{self.item.qty}шт.'
        pixels_price = fm.size(0, text_item_price).width()
        pixels_qty = fm.size(0, text_item_qty).width()
        text_item_name_cut = fm.elidedText(text_item_name, QtCore.Qt.ElideRight, self.width() - 180)

        painter.drawText(QtCore.QRect(0, 0, self.width() - 180, self.height()), QtCore.Qt.AlignVCenter,
                         text_item_name_cut)
        painter.drawText(self.width() - pixels_price - 125, 20, text_item_price)
        painter.drawText(self.width() - pixels_qty - 80, 20, text_item_qty)
        painter.end()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.parent_form.selected_item:
            self.parent_form.selected_item.count_box.hide()
            self.parent_form.selected_item.btn_plus.hide()
        self.parent_form.selected_item = self
        self.count_box.show()
        self.btn_plus.show()
        self.count_box.setFocus()
        self.items = self

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.__color_fon = '#CCC'
        self.update()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.__color_fon = self.__class__.__color_fon
        self.update()

    def on_push_button(self):
        print(self.__parent_form.selected_item)


if __name__ == "__main__":
    from prjstore.domain.item import Item
    from prjstore.domain.product_factory import ProductFactory

    app = QApplication(sys.argv)
    product = ProductFactory.create(id='2', name='item23', price=600)
    item = Item(pr=product, qty=3, buy_price=200)
    w = ItemFrame(parent=None, pr_item=item)
    w.show()
    sys.exit(app.exec_())
