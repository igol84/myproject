import sys

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QSpinBox, QPushButton, QLabel, QLineEdit


class ItemFrame(QWidget):
    default_color_bg = '#E1E1E1'
    default_color_text = '#000'
    color_fon_enter = '#CCC'
    current_color_bg = '#1287A8'
    current_color_text = '#fff'
    height_ = 30
    width_ = 300
    font_family = 'Times'
    font_size = 10

    def __init__(self, parent, pr_item):
        super().__init__()
        self.__parent_form = parent
        self.item = pr_item
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumSize(self.width_, self.height_)
        self.setMaximumHeight(self.height_)
        self.setToolTipDuration(2000)
        self.color_fon = self.default_color_bg
        self.color_text = self.default_color_text
        text_item_description = f'{self.item.product.id}:{self.item.product.name}'
        self.label_item_description = LabelItemDescription(parent=self, text=text_item_description)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.label_item_description.move(5, 0)
        self.price_line_edit = LineEditPrice(str(self.item.product.price.amount), parent=self)
        self.price_line_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.qty_box = qtyBox(self, max_qty=self.item.qty)
        self.btn_plus = QPushButton(parent=self, text='+')
        width = 25 if self.item.qty>1 else 75
        self.btn_plus.setMaximumSize(width, 25)
        self.btn_plus.clicked.connect(self.on_push_button_plus)

        self.price_line_edit.hide()
        self.qty_box.hide()
        self.btn_plus.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def sizeHint(self):
        return QtCore.QSize(self.width_, self.height_)

    def paintEvent(self, e):
        self.qty_box.move(self.width() - self.qty_box.width() - 3 - self.btn_plus.width() - 10, 4)
        self.btn_plus.move(self.width() - self.btn_plus.width() - 3, 3)
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
        text_item_price = f'{self.item.product.price.format_my()}'
        self.qty_box.setRange(1, self.item.qty)
        text_item_qty = f'{self.item.qty}шт.'
        pixels_price = fm.size(0, text_item_price).width()
        pixels_qty = fm.size(0, text_item_qty).width()
        painter.drawText(self.width() - pixels_price - 147, 20, text_item_price)
        self.price_line_edit.move(self.width() - pixels_price - 150, 4)
        painter.drawText(self.width() - pixels_qty - 85, 20, text_item_qty)
        painter.end()

    # on click on this widget
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # change style
        self.color_fon = self.current_color_bg
        self.color_text = self.current_color_text
        self.update()
        # return default style on the previous selected widget
        if self.parent_form and self.parent_form.selected_item_widget \
                and self.parent_form.selected_item_widget is not self:
            self.parent_form.selected_item_widget.color_fon = self.default_color_bg
            self.parent_form.selected_item_widget.color_text = self.default_color_text
            self.parent_form.selected_item_widget.update()
            self.parent_form.selected_item_widget.price_line_edit.hide()
            self.parent_form.selected_item_widget.qty_box.hide()
            self.parent_form.selected_item_widget.btn_plus.hide()
        if self.parent_form:
            self.parent_form.selected_item_widget = self
        if self.item.qty > 1:
            self.qty_box.show()
        self.price_line_edit.show()
        self.btn_plus.show()
        self.qty_box.setFocus()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.color_fon_enter
            self.color_text = self.default_color_text
        self.update()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.default_color_bg
            self.color_text = self.default_color_text
        self.update()

    def on_push_button_plus(self):
        if self.parent_form:
            self.parent_form.put_on_sale()
        self.update()

    def on_pressed_price_line_edit(self):
        if self.price_line_edit.hasFocus():
            self.price_line_edit.clearFocus()
        if self.parent_form:
            self.parent_form.put_on_sale()
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


class qtyBox(QSpinBox):
    def __init__(self, parent, max_qty):
        super().__init__(parent)
        font = self.font()
        font.setPointSize(ItemFrame.font_size)
        self.setFont(font)



class LineEditPrice(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(ItemFrame.font_size)
        self.setFont(font)
        self.setFixedWidth(75)
        validator_reg = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


if __name__ == "__main__":
    from prjstore.domain.item import Item
    from prjstore.domain.product_factory import ProductFactory

    app = QApplication(sys.argv)
    product = ProductFactory.create(product_id='2',
                                    name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!',
                                    price=1600)
    item = Item(pr=product, qty=3, buy_price=200)
    w = ItemFrame(parent=None, pr_item=item)
    w.show()

    # product2 = ProductFactory.create(product_id='2', name='Кроссовки Adidas Y-1 красные', price=10600.50)
    # item2 = Item(pr=product2, qty=1000, buy_price=1200)
    # w2 = ItemFrame(parent=None, pr_item=item2)
    # w2.show()
    sys.exit(app.exec_())
