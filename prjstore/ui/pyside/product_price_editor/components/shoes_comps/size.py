from prjstore.ui.pyside.product_price_editor.components.shoes_comps.shoes_frame_interface import ShoesFrameInterface
from prjstore.ui.pyside.product_price_editor.schemas import ViewSize
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class SizeFrame(ItemFrame):
    pr_id: str
    __price: float
    __size: float
    __selected: bool
    height_ = 30

    def __init__(self, pd_size: ViewSize, shoes_frame=None):
        super().__init__()
        self.shoes_frame: ShoesFrameInterface = shoes_frame
        self.__id = pd_size.prod_id
        self.__size = pd_size.size
        self.__price = pd_size.price
        self.pr_price_format = pd_size.price_format
        self.pr_qty = pd_size.qty
        self.__selected = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(self.height_)
        self.setMinimumWidth(260)

        layer = QHBoxLayout()
        layer.setContentsMargins(4, 4, 4, 4)
        self.label_size = QLabel(f'{self.__size:g}')
        self.label_size.setContentsMargins(5, 0, 5, 0)
        self.label_size.setFixedWidth(50)
        self.label_size.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label_size.setStyleSheet(f'font-size: {self.font_size}pt;')

        self.line_edit_size = QLineEdit(f'{self.__size:g}')
        self.line_edit_size.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_size.hide()
        self.line_edit_size.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_size.setFixedWidth(50)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.line_edit_size.setValidator(validator_reg)

        self.label_qty = QLabel(f'{self.pr_qty}')
        self.label_qty.setContentsMargins(0, 0, 10, 0)
        self.label_qty.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        font = self.label_size.font()
        font.setPointSize(self.font_size)
        self.label_qty.setFont(font)
        self.label_qty.setAlignment(Qt.AlignLeft)

        self.label_price = QLabel(f'{self.pr_price_format}')
        self.label_price.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        font = self.label_size.font()
        font.setPointSize(self.font_size)
        self.label_price.setFont(font)
        self.label_price.setAlignment(Qt.AlignRight)

        self.line_edit_price = QLineEdit(f'{self.__price:g}')
        self.line_edit_price.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_price.hide()
        self.line_edit_price.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_price.setFixedWidth(50)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.line_edit_price.setValidator(validator_reg)

        self.btn = QPushButton('edit')
        self.btn.setStyleSheet(f'background-color: #EEE; color: #000')
        self.btn.hide()
        self.btn.clicked.connect(self.on_clicked_edit)

        layer.addWidget(self.label_size)
        layer.addWidget(self.line_edit_size)
        layer.addWidget(self.label_qty)
        layer.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        layer.addWidget(self.label_price)
        layer.addWidget(self.line_edit_price)
        layer.addWidget(self.btn)
        self.set_default_style()
        self.setLayout(layer)

    def get_id(self) -> str:
        return self.__id

    pr_id = property(get_id)

    def get_price(self) -> float:
        return self.__price

    def set_price(self, price: float) -> None:
        currency = self.label_price.text()[-1]
        self.label_price.setText(f'{price:.2f}' + currency)
        self.line_edit_price.setText(f'{price:g}')
        self.__pr_price = price

    price = property(get_price, set_price)

    def get_size(self) -> float:
        return self.__size

    def set_size(self, size: float) -> None:
        self.label_size.setText(f'{size:g}')
        self.__size = size

    size = property(get_size, set_size)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_selected()
        if self.shoes_frame:
            self.shoes_frame.set_selected_size_frame(self)

    def enterEvent(self, event):
        if not self.selected:
            self.set_hover_style()

    def leaveEvent(self, event):
        if not self.selected:
            self.set_default_style()

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def set_hover_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.color_fon_on_enter}; color: {self.color_text};')

    def set_selected_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.current_color_bg}; color: {self.current_color_text}')

    def on_clicked_edit(self):
        self.selected = False
        if self.shoes_frame:
            self.shoes_frame.edit_size_frame(self)

    def get_selected(self) -> bool:
        return self.__selected

    def set_selected(self, flag: bool = True) -> None:
        if flag:
            self.__selected = True
            self.label_price.hide()
            self.label_size.hide()
            self.line_edit_size.show()
            self.line_edit_price.show()
            self.line_edit_price.setFocus()
            self.line_edit_price.selectAll()
            self.btn.show()
            self.set_selected_style()
        else:
            self.__selected = False
            self.label_price.show()
            self.label_size.show()
            self.line_edit_size.hide()
            self.line_edit_price.hide()
            self.btn.hide()
            self.set_default_style()

    selected = property(get_selected, set_selected)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    view_size = ViewSize(prod_id='14', size=43.5, price=2000, price_format='2.000грн', qty=2)
    frame = SizeFrame(pd_size=view_size)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
