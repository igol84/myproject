import sys

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QFontMetrics, QFont
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QFrame

from prjstore.ui.pyside.sale_registration.components.abstract_product import ItemFrame
from prjstore.ui.pyside.sale_registration.schemas import ViewShoes, ViewSize, ViewWidth, ViewColor


class ShoesFrame(ItemFrame):
    # height_ = 130

    def __init__(self, parent, item_pd: ViewShoes):
        super().__init__()
        self.__parent_form = parent
        self.pr_name = item_pd.name
        self.pr_price = ''
        self.pr_price_format = ''
        self.label_item_description = LabelItemDescription(parent=self, text=self.pr_name)
        self.label_item_description.setFont(QFont(self.color_text, self.font_size))
        self.label_item_description.move(5, 0)
        self.price_line_edit = LineEditPrice(str(self.pr_price), parent=self)

        self.price_line_edit.hide()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def sizeHint(self):
        return QtCore.QSize(self.width_, self.height_)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.color_fon))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
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
    from PySide2.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)

    red_E_sizes = [
        ViewSize(prod_id='2', size=43, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='3', size=44, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='4', size=45, price=2000, price_format='2.000грн', qty=1),
    ]
    red_D_sizes = [
        ViewSize(prod_id='5', size=41, price=4000, price_format='3.000грн', qty=1),
        ViewSize(prod_id='6', size=42, price=4000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='7', size=43, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='8', size=44, price=2000, price_format='2.000грн', qty=1),
    ]
    red_widths = [
        ViewWidth(width='E', sizes=red_E_sizes),
        ViewWidth(width='D', sizes=red_D_sizes),
    ]
    black_E_sizes = [
        ViewSize(prod_id='9', size=43, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='10', size=44, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='11', size=40, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='12', size=41, price=4000, price_format='3.000грн', qty=1),
        ViewSize(prod_id='13', size=42, price=4000, price_format='2.000грн', qty=2),

    ]
    black_D_sizes = [
        ViewSize(prod_id='14', size=43, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='15', size=44, price=2000, price_format='2.000грн', qty=1),
    ]
    black_widths = [
        ViewWidth(width='E', sizes=black_E_sizes),
        ViewWidth(width='D', sizes=black_D_sizes),
    ]
    colors = [
        ViewColor(color='red', widths=red_widths),
        ViewColor(color='black', widths=black_widths),
    ]
    item = ViewShoes(name='Кеды Converse Chuck 70 высокие', colors=colors)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ShoesFrame(parent=None, item_pd=item)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec_())
