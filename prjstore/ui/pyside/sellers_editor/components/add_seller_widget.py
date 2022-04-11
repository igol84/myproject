from prjstore.ui.pyside.sellers_editor.components.ui_add_seller_widget import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class AddSellerWidget(ItemFrame):
    __name: str

    def __init__(self, parent=None):
        super().__init__()
        self.__parent = parent

        self.ui = UI_AddSellerWidget()
        self.ui.setup_ui(self)

        self.set_default_style()
        self.ui.line_edit_name.returnPressed.connect(self.on_pressed_line_name)
        self.ui.line_edit_name.escaped.connect(self.on_escaped_line_name)
        self.ui.btn_add.clicked.connect(self.on_pressed_line_name)

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def __get_name(self) -> str:
        return self.ui.line_edit_name.text()

    def __set_name(self, name: str) -> None:
        self.ui.line_edit_name.setText(name)

    name = property(__get_name, __set_name)

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def on_pressed_line_name(self):
        if self.parent_widget:
            self.parent_widget.on_add_seller(self.name)
        else:
            print(self.name)
        self.ui.line_edit_name.clear()

    def on_escaped_line_name(self):
        self.name = ''


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(480, 320)
    v_box = QVBoxLayout(win)
    frame = AddSellerWidget()
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    v_box.addWidget(frame)
    v_box.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))
    win.show()
    sys.exit(app.exec())
