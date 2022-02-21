from PySide6.QtWidgets import QFrame, QApplication

from prjstore.ui.pyside.login.ui_login import Ui_Frame


class LoginFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui = Ui_Frame()
        ui.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    frame = LoginFrame()
    frame.show()
    sys.exit(app.exec())
