from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QLabel


class LoadImg(QLabel):
    def __init__(self, parent, path):
        super().__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        gif = QtGui.QMovie(path)
        gif.setScaledSize(QtCore.QSize(80, 80))
        self.setFixedSize(gif.scaledSize())
        self.setMovie(gif)
        gif.start()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.move(self.parent().parent().rect().center() - self.rect().center())
        QLabel.paintEvent(self, event)


class LoadWidget(QLabel):
    def __init__(self, parent, path):
        super().__init__(parent=parent)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 50);')
        self.setFixedSize(self.parent().rect().size())
        self.img = LoadImg(parent=self, path=path)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.setFixedSize(self.parent().rect().size())
        QLabel.paintEvent(self, event)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    widget = QWidget()
    win = LoadWidget(parent=widget, path='loading.gif')

    widget.show()
    sys.exit(app.exec())
