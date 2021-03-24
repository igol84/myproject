import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QHBoxLayout, QSpacerItem, QSizePolicy

class ItemFrame(QWidget):
    __color_fon = '#E1E1E1'

    def __init__(self, item, item_frames):
        super().__init__()
        self.item_frames = item_frames
        self.item = item
        self.count_box = QSpinBox()
        self.count_box.setRange(1, self.item.qty)


        self.h_box = QHBoxLayout(self)
        spacer = QSpacerItem(550, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.h_box.addItem(spacer)
        self.h_box.addWidget(self.count_box)
        spacer = QSpacerItem(50, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.h_box.addItem(spacer)
        self.h_box.setContentsMargins(0, 0, 0, 0)

        self.count_box.hide()



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

        painter.drawText(5, 20, self.item.product.name)
        painter.drawText(painter.device().width()-45, 20, f'{self.item.qty}шт.')
        painter.end()

    def _trigger_refresh(self):
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.count_box.show()
        self.count_box.setFocus()
        for frame in self.item_frames:
            if frame is not self:
                frame.count_box.hide()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.__color_fon = '#CCC'
        self.update()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.__color_fon = self.__class__.__color_fon
        self.update()

if __name__ == "__main__":
    from prjstore.domain.item import Item
    from prjstore.domain.product_factory import ProductFactory

    app = QApplication(sys.argv)
    product = ProductFactory.create(id='2', name='item23', price=600)
    item = Item(pr=product, qty=3, buy_price=200)
    w = ItemFrame(item)
    w.show()
    sys.exit(app.exec_())