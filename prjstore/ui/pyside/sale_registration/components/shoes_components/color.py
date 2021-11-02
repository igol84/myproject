from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QSizePolicy, QLabel
from PySide2 import QtWidgets, QtCore

from prjstore.ui.pyside.sale_registration.components.abstract_product import ItemFrame
from prjstore.ui.pyside.sale_registration.components.shoes_components import WidthFrame
from prjstore.ui.pyside.sale_registration.schemas import ViewWidth, ViewColor, ViewSize


class ColorFrame(ItemFrame):
    pd_color: str
    pd_widths: list[ViewWidth]

    def __init__(self, pd_color: ViewColor):
        super().__init__()
        self.pd_color = pd_color.color
        self.pd_widths = pd_color.widths
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(self.sizeHint())
        self.setCursor(QtCore.Qt.ArrowCursor)
        v_layer = QtWidgets.QVBoxLayout()

        if self.pd_color:
            label_color = QLabel(f'{self.pd_color}')
            font = label_color.font()
            font.setPointSize(16)
            font.setItalic(True)
            label_color.setFont(font)
            label_color.setAlignment(QtCore.Qt.AlignCenter)
            v_layer.addWidget(label_color)

        for view_width in self.pd_widths:
            v_layer.addWidget(WidthFrame(pd_width=view_width))

        self.setLayout(v_layer)


if __name__ == '__main__':
    import sys

    E_sizes = [
        ViewSize(prod_id='2', size=43, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='3', size=44, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='4', size=45, price=2000, price_format='2.000грн', qty=1),
    ]
    D_sizes = [
        ViewSize(prod_id='5', size=41, price=4000, price_format='3.000грн', qty=1),
        ViewSize(prod_id='6', size=42.5, price=4000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='7', size=43, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='8', size=44, price=2000, price_format='2.000грн', qty=1),
    ]
    widths = [
        ViewWidth(width='E', sizes=E_sizes),
        ViewWidth(width='D', sizes=D_sizes),
    ]

    view_color = ViewColor(color='Красные', widths=widths)
    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ColorFrame(pd_color=view_color)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec_())
