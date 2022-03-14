from prjstore.ui.pyside.product_price_editor.components.shoes_comps import WidthFrame
from prjstore.ui.pyside.product_price_editor.schemas import ViewWidth, ViewColor, ViewSize
from prjstore.ui.pyside.utils.qt_core import *


class ColorFrame(QFrame):
    __color: str
    pd_widths: list[ViewWidth]
    __selected: bool

    def __init__(self, pd_color: ViewColor, shoes_frame=None):
        super().__init__()
        self.shoes_frame = shoes_frame
        self.__selected = False
        self.__color = pd_color.color
        self.pd_widths = pd_color.widths
        self.frames_of_width: dict[str, WidthFrame] = {}

        layer_widths = QVBoxLayout()
        layer_widths.setContentsMargins(0, 0, 0, 0)
        layer_widths.setSpacing(0)

        self.header = HeaderOfColor(text=f'{self.__color}')
        layer_widths.addWidget(self.header)

        for view_width in self.pd_widths:
            width_frame = WidthFrame(pd_width=view_width, shoes_frame=shoes_frame)
            self.frames_of_width[view_width.width] = width_frame
            layer_widths.addWidget(width_frame)

        self.setLayout(layer_widths)

    def cont_sizes(self):
        return sum([len(width.sizes) for width in self.pd_widths])

    def get_selected(self) -> bool:
        return self.__selected

    def set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.shoes_frame.on_selected_color(self)
            for width in self.frames_of_width.values():
                for size in width.widgets_of_sizes.values():
                    size.selected = False
            self.header.label_color.hide()
            self.header.line_edit_color.show()
            self.header.line_edit_price.show()
            self.header.btn_edit.show()
        else:
            self.header.label_color.show()
            self.header.line_edit_color.hide()
            self.header.line_edit_price.hide()
            self.header.btn_edit.hide()

    selected = property(get_selected, set_selected)

    def get_color(self) -> str:
        return self.__color

    def set_color(self, color: str) -> None:
        self.__color = color
        self.header.set_color(color)

    color = property(get_color, set_color)

    def paintEvent(self, event: QPaintEvent):
        self.header.line_edit_color.setFixedWidth(self.width() - 166)
        return QFrame.paintEvent(self, event)

    def on_color_edit(self):
        self.selected = False
        self.shoes_frame.on_color_edit(self)

    def set_price_of_all_sizes(self, new_price: float):
        for width in self.frames_of_width.values():
            for size in width.widgets_of_sizes.values():
                size.price = new_price


class HeaderOfColor(QWidget):
    def __init__(self, text: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(3, 0, 3, 0)
        self.setCursor(Qt.PointingHandCursor)
        layout = QHBoxLayout(self)
        self.setFixedHeight(35)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.label_color = QLabel(text)
        self.label_color.setStyleSheet('font-size: 17pt;')
        self.label_color.setAlignment(Qt.AlignLeft)
        self.line_edit_color = LineEditColor(parent=self, text=text)
        self.line_edit_color.hide()

        self.line_edit_price = LineEditPrice(parent=self)
        self.line_edit_price.hide()
        self.btn_edit = QPushButton(parent=self, text='edit')
        self.btn_edit.setMaximumSize(75, 25)
        self.btn_edit.hide()
        self.btn_edit.clicked.connect(self.on_push_button_edit)
        layout.addWidget(self.label_color)
        layout.addWidget(self.line_edit_color)
        layout.addWidget(self.line_edit_price)
        layout.addWidget(self.btn_edit)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        parent: ColorFrame = self.parent()
        if parent.selected:
            parent.selected = False
        else:
            parent.selected = True

    def on_push_button_edit(self):
        self.parent().on_color_edit()

    def set_color(self, color: str):
        self.label_color.setText(color)


class LineEditColor(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(50, 24)
        self.setAlignment(Qt.AlignLeft)


class LineEditPrice(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(60, 25)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


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

    view_color = ViewColor(color='Красные ', widths=widths)
    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ColorFrame(pd_color=view_color)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
