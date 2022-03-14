from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtWidgets import QLabel, QLineEdit, QFrame, QPushButton

from prjstore.ui.pyside.product_price_editor.components.shoes_comps.shoes_frame_interface import ShoesFrameInterface


class ShoesDescFrame(QFrame):
    def __init__(self, parent_form=None, shoes_frame=None):
        super().__init__()
        self.__selected: bool = False
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFrameStyle(QFrame.NoFrame)
        self.parent_form = parent_form
        self.parent_shoes_frame = shoes_frame
        self.setFixedHeight(30)
        layer = QtWidgets.QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        self.layer_desc = QtWidgets.QVBoxLayout()
        self.layer_desc.setContentsMargins(3, 3, 3, 3)
        self.label_item_description = LabelItemDescription(text=shoes_frame.name)
        self.label_item_description.setFont(
            QFont(self.parent_shoes_frame.color_text, self.parent_shoes_frame.font_size))
        self.layer_desc.addWidget(self.label_item_description)
        layer.addLayout(self.layer_desc)

        self.line_edit_desc = LineEditDesc(parent=self, text=shoes_frame.name)
        self.line_edit_desc.hide()

        self.price_line_edit = LineEditPrice(parent=self)
        self.price_line_edit.returnPressed.connect(self.on_pressed_price_line_edit)
        self.price_line_edit.hide()
        self.btn_plus = QPushButton(parent=self, text='edit')
        self.btn_plus.setMaximumSize(75, 25)
        self.btn_plus.hide()
        self.btn_plus.clicked.connect(self.on_push_button_edit)
        self.setLayout(layer)

    def __get_shoes_frame(self) -> ShoesFrameInterface:
        return self.parent()

    shoes_frame = property(__get_shoes_frame)

    def set_price(self, price: float):
        self.price_line_edit.setText(f'{price:g}')

    def set_desc(self, name: str):
        self.label_item_description.setText(name)

    def set_data(self, name: str = None, price: float = None):
        if name is not None:
            self.set_desc(name)
        if price is not None:
            self.set_price(price)

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
        self.price_line_edit.move(self.width() - 143, 4)
        self.btn_plus.move(self.width() - self.btn_plus.width() - 3, 3)
        painter.end()
        self.line_edit_desc.setFixedWidth(self.width() - 150)
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
                    self.selected = False
                    return None
                else:
                    self.parent_form.selected_item_widget.color_fon = self.parent_shoes_frame.default_color_bg
                    self.parent_form.selected_item_widget.color_text = self.parent_shoes_frame.default_color_text
                    self.parent_form.selected_item_widget.update()
                    self.parent_form.selected_item_widget.hide_elements()
                    self.parent_form.selected_item_widget.selected = False
            self.parent_form.selected_item_widget = self.parent()
        self.selected = True
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

    def on_push_button_edit(self):
        if self.parent_shoes_frame:
            self.parent_shoes_frame.on_press_edit()
        self.update()

    def get_selected(self) -> bool:
        return self.__selected

    def set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.price_line_edit.show()
            self.btn_plus.show()
            self.label_item_description.hide()
            self.line_edit_desc.show()
        else:
            self.price_line_edit.hide()
            self.btn_plus.hide()
            self.label_item_description.show()
            self.line_edit_desc.hide()

    selected = property(get_selected, set_selected)


class LabelItemDescription(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        self.setToolTip(self.text())
        self.setFixedSize(self.parent().width() - 150, 21)
        painter = QtGui.QPainter(self)
        pen = painter.pen()
        pen.setColor(QtGui.QColor(self.parent().parent_shoes_frame.color_text))
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), QtCore.Qt.ElideRight,
                                         self.parent().parent_shoes_frame.width() - 150)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().parent_shoes_frame.height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)


class LineEditDesc(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(self.parent().parent_shoes_frame.font_size)
        self.setFont(font)
        self.setFixedHeight(23)
        self.move(4, 4)


class LineEditPrice(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(self.parent().parent_shoes_frame.font_size)
        self.setFont(font)
        self.setFixedSize(60, 24)
        validator_reg = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.setValidator(validator_reg)
