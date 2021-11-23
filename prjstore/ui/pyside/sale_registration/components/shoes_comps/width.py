from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QSizePolicy, QLabel, QFrame
from PySide6 import QtWidgets, QtCore

from prjstore.ui.pyside.sale_registration.components.shoes_comps import SizeFrame
from prjstore.ui.pyside.sale_registration.schemas import ViewSize, ViewWidth


class WidthFrame(QFrame):
    pd_sizes: list[ViewSize]
    pr_width: str
    count_in_row = 15

    def __init__(self, pd_width: ViewWidth = '', shoes_frame=None):
        super().__init__()
        self.pr_width = pd_width.width
        self.pd_sizes = pd_width.sizes
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.adjustSize()
        # self.setStyleSheet(f"background-color: #808000")
        layer_widths = QtWidgets.QVBoxLayout()
        layer_widths.setContentsMargins(0, 0, 0, 5)

        if self.pr_width:
            label_width = QLabel(f'{self.pr_width}')
            label_width.setStyleSheet("font-size: 12pt;")
            layer_widths.addWidget(label_width)

        layer_sizes = QtWidgets.QHBoxLayout()
        layer_sizes.setContentsMargins(5, 0, 0, 0)
        layer_sizes.setAlignment(QtCore.Qt.AlignLeft)
        n = 0
        for n, view_size in enumerate(self.pd_sizes, start=1):
            if n % self.count_in_row == 0:
                layer_widths.addLayout(layer_sizes)
                layer_sizes = QtWidgets.QHBoxLayout()
                layer_sizes.setContentsMargins(5, 0, 0, 0)
                layer_sizes.setAlignment(QtCore.Qt.AlignLeft)
            layer_sizes.addWidget(SizeFrame(pd_size=view_size, shoes_frame=shoes_frame))
        if n and n % self.count_in_row != 0:
            layer_widths.addSpacing(5)
            layer_widths.addLayout(layer_sizes)

        self.setLayout(layer_widths)

    def count_sizes(self) -> int:
        return len(self.pd_sizes)


if __name__ == '__main__':
    import sys

    sizes = [
        ViewSize(prod_id='2', size=36, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='3', size=36.5, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='4', size=37, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='5', size=37.5, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='6', size=38, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='7', size=38.5, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='8', size=39, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='9', size=39.5, price=2000, price_format='2.000грн', qty=4),
        ViewSize(prod_id='10', size=40, price=2000, price_format='2.000грн', qty=5),
        ViewSize(prod_id='11', size=40.5, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='12', size=41, price=2000, price_format='2.000грн', qty=3),
        ViewSize(prod_id='13', size=41.5, price=2000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='14', size=42, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='15', size=42.5, price=2000, price_format='2.000грн', qty=3),
        ViewSize(prod_id='16', size=43, price=2000, price_format='2.000грн', qty=5),
        ViewSize(prod_id='17', size=43.5, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='18', size=44, price=2000, price_format='2.000грн', qty=3),
        ViewSize(prod_id='19', size=44.5, price=2000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='20', size=45, price=2000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='21', size=45.5, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='22', size=46, price=2000, price_format='2.000грн', qty=1),
    ]
    view_width = ViewWidth(width='Middle', sizes=sizes)
    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = WidthFrame(pd_width=view_width)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
