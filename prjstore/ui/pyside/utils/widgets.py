from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFontMetrics, QMouseEvent
from PySide6.QtWidgets import QFrame, QLabel


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


class ItemFrame(QFrame):
    default_color_bg = '#E1E1E1'
    default_color_text = '#000'
    color_fon_on_enter = '#CCC'
    current_color_bg = '#1287A8'
    current_color_text = '#fff'
    height_ = 30
    width_ = 300
    font_family = 'Times'
    font_size = 10

    def __init__(self):
        super().__init__()
        self.adjustSize()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.color_fon = self.default_color_bg
        self.color_text = self.default_color_text


class SelectableItemFrame(ItemFrame):
    selected: bool
    def __init__(self):
        super().__init__()
        self.set_default_style()
        self.setObjectName('SelectableFrame')


    def enterEvent(self, event):
        if not self.selected:
            self.set_hover_style()

    def leaveEvent(self, event):
        if not self.selected:
            self.set_default_style()

    def set_default_style(self) -> None:
        self.setStyleSheet(f'QFrame #SelectableFrame '
                           f'{{background-color: {self.default_color_bg};}}')

    def set_hover_style(self) -> None:
        self.setStyleSheet(f'QFrame #SelectableFrame '
                           f'{{background-color: {self.color_fon_on_enter};}}')

    def set_selected_style(self) -> None:
        self.setStyleSheet(f'QFrame #SelectableFrame {{background-color: {self.current_color_bg};}} '
                           f'QFrame QLabel {{color: {self.current_color_text};}}')

    # this all redefine
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.selected = True
        return QFrame.mousePressEvent(self, event)

    def __get_selected(self) -> bool:
        return self.__selected

    def __set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.set_selected_style()
        else:
            self.set_default_style()

    selected = property(__get_selected, __set_selected)


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(2)
        self.setLineWidth(1)


class QVLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedWidth(2)
        self.setLineWidth(1)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    v_box.addWidget(SelectableItemFrame())
    v_box.addWidget(QVLine())
    win.show()
    sys.exit(app.exec())
