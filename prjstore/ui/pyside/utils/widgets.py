from PySide2.QtWidgets import QFrame


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
    from PySide2.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    v_box.addWidget(QHLine())
    v_box.addWidget(QVLine())
    win.show()
    sys.exit(app.exec_())
