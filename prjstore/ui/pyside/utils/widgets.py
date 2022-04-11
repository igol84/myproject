from PySide6 import QtGui, QtCore
from PySide6.QtGui import QFontMetrics
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
    v_box.addWidget(QHLine())
    v_box.addWidget(QVLine())
    win.show()
    sys.exit(app.exec())
