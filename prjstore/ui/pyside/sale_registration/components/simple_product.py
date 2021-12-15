import sys

from PySide6 import QtCore, QtGui
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtWidgets import QWidget, QApplication, QSpinBox, QPushButton, QLabel, QLineEdit, QFrame

from prjstore.ui.pyside.sale_registration.components.abstract_product import AbstractSoldItem
from prjstore.ui.pyside.sale_registration.schemas import ViewProduct
from prjstore.ui.pyside.utils.widgets import ItemFrame


class ProductFrame(ItemFrame, AbstractSoldItem):
    def __init__(self, parent, item_pd: ViewProduct):
        super().__init__()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFixedHeight(self.height_)
        self.setMinimumWidth(300)
        self.__parent_form = parent
        self.pr_id = item_pd.prod_id
        self.pr_name = item_pd.name
        self.pr_price = item_pd.price
        self.pr_price_format = item_pd.price_format
        self.pr_qty = item_pd.qty

        text_item_description = f'{self.pr_id}:{self.pr_name}'
        self.label_item_description = LabelItemDescription(parent=self, text=text_item_description)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.label_item_description.move(5, 0)
        self.price_line_edit = LineEditPrice(f'{self.pr_price:g}', parent=self)
        self.price_line_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.qty_box = QtyBox(self)
        self.btn_plus = QPushButton(parent=self, text='+')
        width = 25 if self.pr_qty > 1 else 75
        self.btn_plus.setMaximumSize(width, 25)
        self.btn_plus.clicked.connect(self.on_push_button_plus)

        self.price_line_edit.hide()
        self.qty_box.hide()
        self.btn_plus.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def get_sale_price(self) -> float:
        return self.price_line_edit.text()

    def get_sale_qty(self) -> int:
        return self.qty_box.text()

    def sizeHint(self):
        return QtCore.QSize(self.width_, self.height_)

    def paintEvent(self, event: QtGui.QPaintEvent):
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

        pen.setColor(QtGui.QColor(self.color_text))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        painter.setFont(font)
        fm = QFontMetrics(font)
        text_item_price = f'{self.pr_price_format}'
        self.qty_box.setRange(1, self.pr_qty)
        text_item_qty = f'{self.pr_qty}шт.'
        pixels_qty = fm.size(0, text_item_qty).width()
        painter.drawText(self.width() - 211, 20, text_item_price)
        self.price_line_edit.move(self.width() - 211, 4)
        painter.drawText(self.width() - pixels_qty - 85, 20, text_item_qty)
        painter.end()
        return QFrame.paintEvent(self, event)

    # on click on this widget
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
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
            if self.pr_qty > 1:
                self.qty_box.show()
            self.price_line_edit.show()
            self.btn_plus.show()
        self.price_line_edit.setFocus()
        self.price_line_edit.selectAll()

    def hide_elements(self):
        self.price_line_edit.hide()
        self.qty_box.hide()
        self.btn_plus.hide()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.color_fon_on_enter
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

    def on_press_enter_on_qty_box_edit(self):
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


class QtyBox(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)
        font = self.font()
        font.setPointSize(ProductFrame.font_size)
        self.setFont(font)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Enter:
            self.clearFocus()
            self.parent().on_press_enter_on_qty_box_edit()
        else:
            QSpinBox.keyPressEvent(self, event)


class LineEditPrice(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(ProductFrame.font_size)
        self.setFont(font)
        self.setFixedSize(75, 24)
        validator_reg = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


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
