import sys

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QLineEdit

from prjstore.ui.pyside.sale_registration.schemas import ViewShoes


class ShoesFrame(QWidget):
    default_color_bg = '#E1E1E1'
    default_color_text = '#000'
    color_fon_enter = '#CCC'
    current_color_bg = '#1287A8'
    current_color_text = '#fff'
    height_ = 30
    width_ = 300
    font_family = 'Times'
    font_size = 10

    def __init__(self, parent, item: ViewShoes):
        super().__init__()
        self.__parent_form = parent
        self.pr_name = item.name
        self.pr_price = ''
        self.pr_price_format = ''
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMinimumSize(self.width_, self.height_)
        self.color_fon = self.default_color_bg
        self.color_text = self.default_color_text
        text_item_description = f'{self.pr_name}'
        self.label_item_description = LabelItemDescription(parent=self, text=text_item_description)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.label_item_description.move(5, 0)
        self.price_line_edit = LineEditPrice(str(self.pr_price), parent=self)

        self.price_line_edit.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def sizeHint(self):
        return QtCore.QSize(self.width_, self.height_)

    def paintEvent(self, e):
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
        text_item_price = f'{self.pr_price_format}'
        painter.drawText(self.width() - 100, 20, text_item_price)
        self.price_line_edit.move(self.width() - 100, 4)
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
            self.parent_form.selected_item_widget.hide_elements()
        if self.parent_form:
            self.parent_form.selected_item_widget = self
        self.price_line_edit.show()
        self.price_line_edit.setFocus()
        self.price_line_edit.selectAll()

    def hide_elements(self):
        self.price_line_edit.hide()

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


class LabelItemDescription(QLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        painter = QtGui.QPainter(self)
        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.parent().color_text))
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), QtCore.Qt.ElideRight, self.parent().width() - 100)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)


class LineEditPrice(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(ShoesFrame.font_size)
        self.setFont(font)
        self.setFixedWidth(75)
        validator_reg = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ShoesFrame(parent=None, pr_id=2, pr_name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!',
                   pr_price=1600, pr_price_format='1600 грн.', pr_qty=3)
    w.show()
    sys.exit(app.exec_())
