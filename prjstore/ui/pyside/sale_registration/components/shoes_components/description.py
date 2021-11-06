from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QFrame

from prjstore.ui.pyside.sale_registration.components.abstract_product import ItemFrame
from prjstore.ui.pyside.sale_registration.components.shoes_components.shoes_frame_interface import ShoesFrameInterface


class ShoesDesc(ItemFrame):
    # height_ = 130
    pr_name: str
    pr_price: float

    def __init__(self, parent=None, pr_name: str = ''):
        super().__init__()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFrameStyle(QFrame.NoFrame)
        self.parent_form = parent
        self.pr_name = pr_name
        self.pr_price_format = ''
        self.setFixedHeight(30)
        layer = QtWidgets.QVBoxLayout()
        layer.setMargin(0)
        self.layer_desc = QtWidgets.QVBoxLayout()
        self.layer_desc.setMargin(3)
        self.label_item_description = LabelItemDescription(text=self.pr_name)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.layer_desc.addWidget(self.label_item_description)
        layer.addLayout(self.layer_desc)
        self.price_line_edit = LineEditPrice(parent=self, text='0')
        self.price_line_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.price_line_edit.hide()
        self.setLayout(layer)

    def __get_shoes_frame(self) -> ShoesFrameInterface:
        return self.parent()

    shoes_frame = property(__get_shoes_frame)

    def set_price(self, price: float):
        self.price_line_edit.text(f'{price:g}')

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), 30)
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.color_text))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        painter.setFont(font)
        self.price_line_edit.move(self.width() - 100, 4)
        painter.end()
        return QFrame.paintEvent(self, event)

    # on click on this widget
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # change style
        self.color_fon = self.current_color_bg
        self.color_text = self.current_color_text

        # return default style on the previous selected widget
        if self.parent_form:
            if self.parent_form.selected_item_widget:
                if self.parent_form.selected_item_widget is self:
                    self.color_fon = self.color_fon_on_enter
                    self.color_text = self.default_color_text
                    self.parent_form.selected_item_widget.hide_elements()
                    self.parent_form.selected_item_widget = None
                    self.shoes_frame.hide_colors()
                    return None
                else:
                    self.parent_form.selected_item_widget.color_fon = self.default_color_bg
                    self.parent_form.selected_item_widget.color_text = self.default_color_text
                    self.parent_form.selected_item_widget.update()
                    self.parent_form.selected_item_widget.hide_elements()
            self.parent_form.selected_item_widget = self
            self.shoes_frame.show_colors()
        return QFrame.mousePressEvent(self, event)

    def hide_elements(self):
        self.price_line_edit.hide()
        self.shoes_frame.hide_colors()

    def enterEvent(self, event: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.color_fon_on_enter
            self.color_text = self.default_color_text
            self.update()
        return QFrame.enterEvent(self, event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self:
            self.color_fon = self.default_color_bg
            self.color_text = self.default_color_text
            self.update()
        return QFrame.enterEvent(self, event)

    def on_pressed_price_line_edit(self):
        print(self.price_line_edit.text())


class LabelItemDescription(QLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        self.setFixedSize(self.parent().width() - 100, 21)
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
        font.setPointSize(ShoesDesc.font_size)
        self.setFont(font)
        self.setFixedSize(75, 22)
        validator_reg = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ShoesDesc(pr_name='Кеды Converse Chuck 70 высокие высокие высокие высокие')
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec_())
