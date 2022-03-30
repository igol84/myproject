from prjstore.ui.pyside.product_price_editor.components.shoes_comps.shoes_frame_interface import ShoesFrameInterface
from prjstore.ui.pyside.product_price_editor.schemas import ViewProduct
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class ProductFrame(ItemFrame, ShoesFrameInterface):
    __id: str
    __name: str
    __price: float
    __selected: bool
    height_ = 30

    def __init__(self, item_pd: ViewProduct, parent=None):
        super().__init__()
        self.__parent_form = parent
        self.__id = item_pd.prod_id
        self.__name = item_pd.name
        self.__price = item_pd.price
        self.pr_price_format = item_pd.price_format
        self.pr_qty = item_pd.qty
        self.__selected = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(self.height_)
        self.setMinimumWidth(260)

        layer = QHBoxLayout()
        layer.setContentsMargins(0, 0, 5, 0)
        self.label_name = QLabel(self.__name)
        self.label_name.setContentsMargins(5, 0, 5, 0)
        self.label_name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.label_name.setStyleSheet(f'font-size: {self.font_size}pt;')
        self.label_name.setAlignment(Qt.AlignLeft)

        self.line_edit_name = QLineEdit(self.__name)
        self.line_edit_name.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_name.hide()
        self.line_edit_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.label_qty = QLabel(f'{self.pr_qty}шт.')
        self.label_qty.setContentsMargins(0, 0, 10, 0)
        self.label_qty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        font = self.label_name.font()
        font.setPointSize(self.font_size)
        self.label_qty.setFont(font)
        self.label_qty.setAlignment(Qt.AlignLeft)
        self.label_qty.setFixedWidth(50)

        self.label_price = QLabel(f'{self.pr_price_format}')
        self.label_price.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        font = self.label_name.font()
        font.setPointSize(self.font_size)
        self.label_price.setFont(font)
        self.label_price.setAlignment(Qt.AlignRight)

        self.line_edit_price = QLineEdit(f'{self.__price:g}')
        self.line_edit_price.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_price.hide()
        self.line_edit_price.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.line_edit_price.setFixedWidth(50)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.line_edit_price.setValidator(validator_reg)

        self.btn = QPushButton('edit')
        self.btn.setStyleSheet(f'background-color: #EEE; color: #000')
        self.btn.hide()
        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.clicked.connect(self.on_clicked_edit)

        layer.addWidget(self.label_name)
        layer.addWidget(self.line_edit_name)
        layer.addWidget(self.label_qty)
        layer.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Preferred, QSizePolicy.Fixed))
        layer.addWidget(self.label_price)
        layer.addWidget(self.line_edit_price)
        layer.addWidget(self.btn)
        self.set_default_style()
        self.setLayout(layer)

    def get_parent(self):
        return self.__parent_form

    parent_form = property(get_parent)

    def get_id(self) -> str:
        return self.__id

    pr_id = property(get_id)

    def get_name(self) -> float:
        return self.__name

    def set_name(self, name: float) -> None:
        self.__name = name
        self.label_name.setText(name)

    name = property(get_name, set_name)

    def get_price(self) -> float:
        return self.__price

    def set_price(self, price: float) -> None:
        self.__price = price
        currency = self.label_price.text()[-1]
        self.label_price.setText(f'{price:.2f}' + currency)

    price = property(get_price, set_price)

    def hide_elements(self):
        self.selected = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.parent_form:
            if self.parent_form.selected_item_widget:
                self.parent_form.selected_item_widget.hide_elements()
                if self.parent_form.selected_item_widget is self:
                    self.parent_form.selected_item_widget = None
                    self.selected = False
                    return None
            self.parent_form.selected_item_widget = self
        self.selected = True
        return QFrame.mousePressEvent(self, event)

    def enterEvent(self, event):
        if not self.selected:
            self.set_hover_style()

    def leaveEvent(self, event):
        if not self.selected:
            self.set_default_style()

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def set_hover_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.color_fon_on_enter}; color: {self.default_color_text};')

    def set_selected_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.current_color_bg}; color: {self.current_color_text}')

    def on_clicked_edit(self):
        self.selected = False
        if self.parent_form:
            self.parent_form.on_press_edit_simple_product(self)
            self.parent_form.selected_item_widget = None

    def get_selected(self) -> bool:
        return self.__selected

    def set_selected(self, flag: bool = True) -> None:
        if flag:
            self.__selected = True
            self.label_price.hide()
            self.label_name.hide()
            self.line_edit_name.show()
            self.line_edit_price.show()
            self.line_edit_price.setFocus()
            self.line_edit_price.selectAll()
            self.btn.show()
            self.set_selected_style()
        else:
            self.__selected = False
            self.label_price.show()
            self.label_name.show()
            self.line_edit_name.hide()
            self.line_edit_price.hide()
            self.btn.hide()
            self.set_default_style()

    selected = property(get_selected, set_selected)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    pd_product = ViewProduct(prod_id='12', name='battery', price=122.6, price_format='126.60$', qty=5)
    frame = ProductFrame(item_pd=pd_product)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
