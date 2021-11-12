import sys

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit


class SLI_Frame(QWidget):
    sli_product_id: str
    sli_product_name: str
    sli_price: float
    sli_price_format: str
    sli_qty: int

    default_color_bg = '#E1E1E1'
    default_color_text = '#000'
    color_fon_enter = '#CCC'
    current_color_bg = '#1287A8'
    current_color_text = '#fff'
    height_ = 30
    width_ = 300
    font_family = 'Times'
    font_size = 10

    def __init__(self, parent, sli_product_id: int, sli_desc: str, sli_sale_price: float,
                 sli_sale_price_format: str, sli_qty: int):
        super().__init__()
        self.__parent_form = parent
        self.sli_product_id = sli_product_id
        self.sli_price = sli_sale_price
        self.sli_price_format = sli_sale_price_format
        self.sli_qty = sli_qty
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumSize(self.width_, self.height_)
        self.color_fon = self.default_color_bg
        self.color_text = self.default_color_text
        self.label_item_description = LabelItemDescription(parent=self, text=sli_desc)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.label_item_description.move(5, 0)
        self.price_edit = LineEditPrice(self.sli_price, parent=self)
        self.price_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.btn_minus = QPushButton(parent=self, text='-')
        self.btn_minus.setMaximumSize(75, 25)
        self.btn_minus.clicked.connect(self.on_push_button_plus)
        self.btn_minus.hide()
        self.price_edit.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def sizeHint(self):
        return QtCore.QSize(self.width_, self.height_)

    def paintEvent(self, e):
        self.btn_minus.move(self.width() - self.btn_minus.width() - 3, 3)
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('#555'))
        painter.setPen(pen)
        painter.drawRect(-1, -1, painter.device().width() - 1, painter.device().height() - 1)

        pen.setColor(QtGui.QColor(self.color_text))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        painter.setFont(font)
        fm = QFontMetrics(font)
        text_sale_price = f'{self.sli_price_format}'
        text_item_qty = f'{self.sli_qty}шт.'
        pixels_qty = fm.size(0, text_item_qty).width()
        painter.drawText(self.width() - 211, 20, text_sale_price)
        self.price_edit.move(self.width() - 214, 4)
        painter.drawText(self.width() - pixels_qty - 85, 20, text_item_qty)
        painter.end()

    # on click on this widget
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # change style
        self.color_fon = self.current_color_bg
        self.color_text = self.current_color_text
        self.update()
        # return default style on the previous selected widget
        if self.parent_form and self.parent_form.selected_sli_widget \
                and self.parent_form.selected_sli_widget is not self:
            self.parent_form.selected_sli_widget.color_fon = self.default_color_bg
            self.parent_form.selected_sli_widget.color_text = self.default_color_text
            self.parent_form.selected_sli_widget.update()
            self.parent_form.selected_sli_widget.price_edit.hide()
            self.parent_form.selected_sli_widget.btn_minus.hide()
        if self.parent_form:
            self.parent_form.selected_sli_widget = self
        self.price_edit.show()
        self.btn_minus.show()
        self.price_edit.setFocus()
        self.price_edit.selectAll()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_sli_widget is not self:
            self.color_fon = self.color_fon_enter
            self.color_text = self.default_color_text
        self.update()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_sli_widget is not self:
            self.color_fon = self.default_color_bg
            self.color_text = self.default_color_text
        self.update()

    def on_pressed_price_line_edit(self):
        self.parent_form.edit_sale_price_in_sli(self.sli_product_id, self.sli_price, float(self.price_edit.text()))
        self.parent_form.selected_sli_widget = None
        self.btn_minus.hide()
        self.price_edit.hide()
        self.update()

    def on_push_button_plus(self):
        if self.parent_form:
            self.parent_form.put_item_form_sli_to_items()
        self.update()


class LabelItemDescription(QLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        painter = QtGui.QPainter(self)
        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.parent().color_text))
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), QtCore.Qt.ElideRight, self.parent().width() - 220)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)


class LineEditPrice(QLineEdit):
    def __init__(self, price, parent):
        super().__init__(str(price), parent)
        font = self.font()
        font.setPointSize(SLI_Frame.font_size)
        self.setFont(font)
        self.setFixedWidth(75)
        validator_reg = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SLI_Frame(parent=None, sli_product_id=2,
                  sli_product_name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!',
                  sli_sale_price=200, sli_sale_price_format='200 грн.', sli_qty=2)
    w.show()

    # product2 = ProductFactory.create(product_id='2', name='Кроссовки Adidas Y-1 красные', price=10600.50)
    # item2 = Item(pr=product2, qty=1000, buy_price=1200)
    # w2 = ItemFrame(parent=None, pr_item=item2)
    # w2.show()
    sys.exit(app.exec_())
