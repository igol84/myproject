from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtWidgets import QLabel, QLineEdit, QFrame, QPushButton

from prjstore.ui.pyside.sale_registration.components.shoes_comps.shoes_frame_interface import ShoesFrameInterface


class ShoesDescFrame(QFrame):
    pr_name: str
    pr_price: float

    def __init__(self, parent_form=None, shoes_frame=None):
        super().__init__()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFrameStyle(QFrame.NoFrame)
        self.parent_form = parent_form
        self.parent_shoes_frame = shoes_frame
        self.pr_name = shoes_frame.pr_name
        self.setFixedHeight(30)
        layer = QtWidgets.QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        self.layer_desc = QtWidgets.QVBoxLayout()
        self.layer_desc.setContentsMargins(3, 3, 3, 3)
        self.label_item_description = LabelItemDescription(text=self.pr_name)
        self.label_item_description.setFont(
            QFont(self.parent_shoes_frame.color_text, self.parent_shoes_frame.font_size))
        self.layer_desc.addWidget(self.label_item_description)
        layer.addLayout(self.layer_desc)
        self.price_line_edit = LineEditPrice(parent=self, text='0')
        self.price_line_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.price_line_edit.hide()
        self.btn_plus = QPushButton(parent=self, text='+')
        self.btn_plus.setMaximumSize(25, 25)
        self.btn_plus.hide()
        self.btn_plus.clicked.connect(self.on_push_button_plus)
        self.setLayout(layer)

    def __get_shoes_frame(self) -> ShoesFrameInterface:
        return self.parent()

    shoes_frame = property(__get_shoes_frame)

    def set_price(self, price: float):
        self.price_line_edit.text(f'{price:g}')

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.parent().color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), 30)
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.parent().color_text))
        painter.setPen(pen)
        font = painter.font()
        font.setFamily(self.parent().font_family)
        font.setPointSize(self.parent().font_size)
        painter.setFont(font)
        self.price_line_edit.move(self.width() - 100, 4)
        self.btn_plus.move(self.width() - self.btn_plus.width() - 3, 3)
        painter.end()
        return QFrame.paintEvent(self, event)

    # on click on this widget
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # change style
        self.parent_shoes_frame.color_fon = self.parent_shoes_frame.current_color_bg
        self.parent_shoes_frame.color_text = self.parent_shoes_frame.current_color_text

        # return default style on the previous selected widget
        if self.parent_form:
            if self.parent_form.selected_item_widget:
                if self.parent_form.selected_item_widget is self.parent():
                    self.parent().color_fon = self.parent_shoes_frame.color_fon_on_enter
                    self.parent().color_text = self.parent_shoes_frame.default_color_text
                    self.parent_form.selected_item_widget.hide_elements()
                    self.parent_form.selected_item_widget = None
                    self.shoes_frame.hide_colors()
                    return None
                else:
                    self.parent_form.selected_item_widget.color_fon = self.parent_shoes_frame.default_color_bg
                    self.parent_form.selected_item_widget.color_text = self.parent_shoes_frame.default_color_text
                    self.parent_form.selected_item_widget.update()
                    self.parent_form.selected_item_widget.hide_elements()
            self.parent_form.selected_item_widget = self.parent()
        self.shoes_frame.show_colors()
        return QFrame.mousePressEvent(self, event)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self.parent_shoes_frame:
            self.parent_shoes_frame.color_fon = self.parent_shoes_frame.color_fon_on_enter
            self.parent_shoes_frame.color_text = self.parent_shoes_frame.default_color_text
            self.update()
        return QFrame.enterEvent(self, event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.parent_form and self.parent_form.selected_item_widget is not self.parent_shoes_frame:
            self.parent_shoes_frame.color_fon = self.parent_shoes_frame.default_color_bg
            self.parent_shoes_frame.color_text = self.parent_shoes_frame.default_color_text
            self.update()

    def on_pressed_price_line_edit(self):
        if self.price_line_edit.hasFocus():
            self.price_line_edit.clearFocus()
        if self.parent_form:
            self.parent_form.put_on_sale()
        self.update()

    def on_push_button_plus(self):
        if self.parent_form:
            self.parent_form.put_on_sale()
        self.update()


class LabelItemDescription(QLabel):
    def paintEvent(self, event):
        self.setToolTip(self.text())
        self.setFixedSize(self.parent().width() - 100, 21)
        painter = QtGui.QPainter(self)
        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.parent().parent_shoes_frame.color_text))
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), QtCore.Qt.ElideRight,
                                         self.parent().parent_shoes_frame.width() - 100)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().parent_shoes_frame.height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)


class LineEditPrice(QLineEdit):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(self.parent().parent_shoes_frame.font_size)
        self.setFont(font)
        self.setFixedSize(60, 24)
        validator_reg = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)
