import sys

from prjstore.ui.pyside.product_price_editor.components.abstract_product import AbstractItem
from prjstore.ui.pyside.product_price_editor.schemas import ViewProduct
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class ProductFrame(ItemFrame, AbstractItem):
    def __init__(self, item_pd: ViewProduct, parent=None):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(self.height_)
        self.setMinimumWidth(300)
        self.__parent_form = parent
        self.pr_id = item_pd.prod_id
        self.pr_name = item_pd.name
        self.pr_price = item_pd.price
        self.pr_price_format = item_pd.price_format
        self.pr_qty = item_pd.qty

        text_item_description = f'{self.pr_name}'
        self.label_product_description = LabelItemDescription(parent=self, text=text_item_description)
        self.label_product_description.setFont(QFont(self.color_text, self.font_size))
        self.label_product_description.move(5, 0)
        self.line_edit_product_description = LineEditProductDesc(parent=self, text=text_item_description)
        self.line_edit_price = LineEditPrice(f'{self.pr_price:g}', parent=self)
        self.line_edit_price.returnPressed.connect(self.on_pressed_price_line_edit)
        self.btn_edit = QPushButton(parent=self, text='edit')
        self.btn_edit.setMaximumSize(75, 25)
        self.btn_edit.clicked.connect(self.on_push_button_edit)

        self.line_edit_product_description.hide()
        self.line_edit_price.hide()
        self.btn_edit.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def get_sale_price(self) -> float:
        return self.line_edit_price.text()

    def sizeHint(self):
        return QSize(self.width_, self.height_)

    def paintEvent(self, event: QPaintEvent):
        self.btn_edit.move(self.width() - self.btn_edit.width() - 3, 3)
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(self.color_fon))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QColor('#555'))
        painter.setPen(pen)

        pen.setColor(QColor(self.color_text))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        painter.setFont(font)
        fm = QFontMetrics(font)
        text_item_price = f'{self.pr_price_format}'
        text_item_qty = f'{self.pr_qty}шт.'
        pixels_qty = fm.size(0, text_item_qty).width()
        painter.drawText(self.width() - 211, 20, text_item_price)
        painter.drawText(self.width() - pixels_qty - 85, 20, text_item_qty)
        painter.end()
        self.line_edit_price.move(self.width() - 211, 4)
        self.line_edit_product_description.setFixedWidth(self.width() - 216)
        return QFrame.paintEvent(self, event)

    # on click on this widget
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # change style
        self.color_fon = self.current_color_bg
        self.color_text = self.current_color_text
        self.update()
        # return default style on the previous selected widget
        if self.parent_form:
            if self.parent_form.selected_item_widget:
                if self.parent_form.selected_item_widget is not self:
                    self.parent_form.selected_item_widget.color_fon = self.default_color_bg
                    self.parent_form.selected_item_widget.color_text = self.default_color_text
                    self.parent_form.selected_item_widget.update()
                    self.parent_form.selected_item_widget.hide_elements()
            self.parent_form.selected_item_widget = self
        self.line_edit_price.show()
        self.line_edit_product_description.show()
        self.btn_edit.show()
        self.line_edit_price.setFocus()
        self.line_edit_price.selectAll()

    def hide_elements(self):
        self.line_edit_product_description.hide()
        self.line_edit_price.hide()
        self.btn_edit.hide()

    def enterEvent(self, a0: QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.color_fon_on_enter
            self.color_text = self.default_color_text
        self.update()

    def leaveEvent(self, a0: QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.default_color_bg
            self.color_text = self.default_color_text
        self.update()

    def on_push_button_edit(self):
        if self.parent_form:
            print('clik!')
        self.update()

    def on_pressed_price_line_edit(self):
        if self.line_edit_price.hasFocus():
            self.line_edit_price.clearFocus()
        self.on_push_button_edit()

        self.update()


class LabelItemDescription(QLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        painter = QPainter(self)
        pen = painter.pen()
        pen.setColor(QColor(self.parent().color_text))
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), Qt.ElideRight, self.parent().width() - 220)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)


class LineEditPrice(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(ProductFrame.font_size)
        self.setFont(font)
        self.setFixedSize(75, 24)
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


class LineEditProductDesc(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(ProductFrame.font_size)
        self.setFont(font)
        self.move(4, 4)
        self.setFixedHeight(24)
        self.home(False)


if __name__ == "__main__":
    from PySide6.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)
    product = ViewProduct(type='product', prod_id='2', price=1600, price_format='1600 грн.', qty=3,
                          name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!')
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ProductFrame(parent=None, item_pd=product)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
