import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton

class ItemFrame(QWidget):
    __color_fon = '#E1E1E1'
    selected_item = None
    sale_form = None

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.setToolTip(self.item.product.name)
        self.setToolTipDuration(2000)
        self.count_box = QSpinBox()
        self.count_box.setRange(1, self.item.qty)
        self.btn_plus = QPushButton('+')
        self.btn_plus.setMaximumSize(25, 25)
        self.btn_plus.clicked.connect(self.on_push_button)

        self.count_box.setRange(1, self.item.qty)


        self.h_box = QHBoxLayout(self)
        spacer = QSpacerItem(1500, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.h_box.addItem(spacer)
        self.h_box.addWidget(self.count_box)
        self.h_box.addWidget(self.btn_plus)
        spacer = QSpacerItem(50, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.h_box.addItem(spacer)
        self.h_box.setContentsMargins(0, 0, 0, 0)

        self.count_box.hide()
        self.btn_plus.hide()



    def sizeHint(self):
        return QtCore.QSize(700, 30)

    def paintEvent(self, e):
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
        pixelsWide = fm.width(f'{self.item.product.price.format_my()}')


        painter.drawText(QtCore.QRect(0, 0, painter.device().width()-180, 25), QtCore.Qt.AlignVCenter,
                         f'{self.item.product.id}:{self.item.product.name}')
        # painter.drawText(5, 20, f'{self.item.product.id}:{self.item.product.name}')
        painter.drawText(painter.device().width()-pixelsWide-125, 20, f'{self.item.product.price.format_my()}')
        painter.drawText(painter.device().width()-45, 20, f'{self.item.qty}шт.')
        painter.end()


    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.__class__.selected_item:
            self.__class__.selected_item.count_box.hide()
            self.__class__.selected_item.btn_plus.hide()
        self.__class__.selected_item = self
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

        print(self.__class__.sale_form.handler.store.items[self.item.product.id])

if __name__ == "__main__":
    from prjstore.domain.item import Item
    from prjstore.domain.product_factory import ProductFactory

    app = QApplication(sys.argv)
    product = ProductFactory.create(id='2', name='item23', price=600)
    item = Item(pr=product, qty=3, buy_price=200)
    w = ItemFrame(item)
    w.show()
    sys.exit(app.exec_())