import sys

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QRect
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QSpinBox, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton

class ItemFrame(QWidget):
    __color_fon = '#E1E1E1'
    parent_form = None
    __h = 30
    __w = 300

    def __init__(self, item):
        super().__init__()
        self.item = item
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



    def sizeHint(self):
        return QtCore.QSize(self.__w, self.__h)

    def paintEvent(self, e):
        self.count_box.move(self.width()-self.count_box.width()-3-self.btn_plus.width()-3, 4)
        self.btn_plus.move(self.width()-self.btn_plus.width()-3, 3)
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.__color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(),
                            painter.device().height())
        painter.fillRect(rect, brush)


        pen = painter.pen()
        pen.setColor(QtGui.QColor('#555'))
        painter.setPen(pen)
        painter.drawRect(-1, -1, painter.device().width()-1, painter.device().height()-1)

        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)
        fm = QFontMetrics(font)
        pixels_price = fm.width(f'{self.item.product.price.format_my()}')
        pixels_qty = fm.width(f'{self.item.qty}шт.')

        text_name = f'{self.item.product.id}:{self.item.product.name}'
        elided = fm.elidedText(text_name, QtCore.Qt.ElideRight, self.width()-180)
        painter.drawText(QtCore.QRect(0, 0, self.width()-180, self.height()), QtCore.Qt.AlignVCenter, elided)
        painter.drawText(self.width()-pixels_price-125, 20, f'{self.item.product.price.format_my()}')
        painter.drawText(self.width()-pixels_qty-80, 20, f'{self.item.qty}шт.')
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
        print(self.parent_form.selected_item)

if __name__ == "__main__":
    from prjstore.domain.item import Item
    from prjstore.domain.product_factory import ProductFactory

    app = QApplication(sys.argv)
    product = ProductFactory.create(id='2', name='item23', price=600)
    item = Item(pr=product, qty=3, buy_price=200)
    w = ItemFrame(item)
    w.show()
    sys.exit(app.exec_())