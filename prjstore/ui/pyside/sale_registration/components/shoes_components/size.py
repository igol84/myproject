from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QSizePolicy
from PySide2 import QtWidgets, QtCore, QtGui

from prjstore.ui.pyside.sale_registration.components.abstract_product import ItemFrame
from prjstore.ui.pyside.sale_registration.components.shoes_components.shoes_frame_interface import ShoesFrameInterface
from prjstore.ui.pyside.sale_registration.schemas import ViewSize
from prjstore.ui.pyside.utils.widgets import QHLine


class SizeFrame(ItemFrame):
    pr_size: float
    height_ = 50
    width_ = 30

    def __init__(self, pd_size: ViewSize, shoes_frame=None):
        super().__init__()
        self.shoes_frame: ShoesFrameInterface = shoes_frame
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

        line = QHLine()

        label_qty = QLabel(f'{self.pr_qty}')
        font = label_size.font()
        font.setPointSize(self.font_size)
        label_qty.setFont(font)
        label_qty.setAlignment(QtCore.Qt.AlignCenter)

        layer.addWidget(label_size)
        layer.addWidget(line)
        layer.addWidget(label_qty)
        self.setLayout(layer)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.shoes_frame:
            self.shoes_frame.set_selected_size_frame(self)
        # change style


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
