from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QSizePolicy, QFrame
from PySide2 import QtWidgets, QtCore

from prjstore.ui.pyside.sale_registration.components.abstract_product import Item, ItemFrame
from prjstore.ui.pyside.sale_registration.schemas import ViewSize


class SizeFrame(ItemFrame, Item):
    pr_size: float
    height_ = 50
    width_ = 30

    def __init__(self, pd_size: ViewSize):
        super().__init__()
        self.pr_id = pd_size.prod_id
        self.pr_size = pd_size.size
        self.pr_price = pd_size.price
        self.pr_qty = pd_size.qty
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        layer = QtWidgets.QVBoxLayout()
        layer.setMargin(4)
        layer.setSpacing(2)

        label_size = QLabel(f'{self.pr_size:g}')
        font = label_size.font()
        font.setPointSize(self.font_size)
        label_size.setFont(font)
        label_size.setAlignment(QtCore.Qt.AlignCenter)

        line = QFrame()
        line.setFixedHeight(2)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        label_qty = QLabel(f'{self.pr_qty}')
        font = label_size.font()
        font.setPointSize(self.font_size)
        label_qty.setFont(font)
        label_qty.setAlignment(QtCore.Qt.AlignCenter)

        layer.addWidget(label_size)
        layer.addWidget(line)
        layer.addWidget(label_qty)
        self.setLayout(layer)

    def get_sale_price(self) -> float:
        ...


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    view_size = ViewSize(prod_id='14', size=43.5, price=2000, price_format='2.000грн', qty=2)
    frame = SizeFrame(pd_size=view_size)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec_())
