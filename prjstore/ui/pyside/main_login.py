import os

from PySide6.QtWidgets import QFrame, QApplication

from prjstore.ui.pyside.login.ui_login import Ui_Frame
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface


class LoginFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()
        self.parent: MainWindowInterface = parent
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        self.ui.ok.clicked.connect(self.save_user_data)
        path = os.getenv('APPDATA')
        folder = 'pystore'
        file_name = 'data'
        folder_path = os.path.join(path, folder)
        self.file_path = os.path.normpath(os.path.join(folder_path, file_name))
        mame, password = '', ''

        # check and create file if not exist
        if os.path.isdir(folder_path):
            if os.path.isfile(self.file_path):
                num_lines = sum(1 for _ in open(self.file_path))
                if num_lines == 2:
                    with open(self.file_path, 'r') as file:
                        mame, password = [line.strip() for line in file]
                else:
                    open(self.file_path, 'a').close()
            else:
                open(self.file_path, 'a').close()
        else:
            os.mkdir(folder_path)
            open(self.file_path, 'a').close()

        self.ui.name.setText(mame)
        self.ui.passw.setText(password)

    def get_name(self) -> str:
        return self.ui.name.text()

    def set_name(self, name: str):
        self.ui.name.setText(name)

    name = property(get_name, set_name)

    def get_user_data(self) -> dict:
        name = self.ui.name.text() if self.ui.name.text() else 'name'
        password = self.ui.passw.text() if self.ui.passw.text() else 'password'
        return {'username': name, 'password': password}

    def save_user_data(self):
        name = self.ui.name.text()
        password = self.ui.passw.text()
        with open(self.file_path, 'w') as f:
            f.write(f'{name} \n{password} ')
        if self.parent:
            self.parent.start_connection()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    frame = LoginFrame()
    frame.show()

    sys.exit(app.exec())
