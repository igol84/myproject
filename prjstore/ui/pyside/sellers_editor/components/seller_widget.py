from prjstore.ui.pyside.sellers_editor.components.ui_seller_widget import *
from prjstore.ui.pyside.sellers_editor.schemas import ViewSeller
from prjstore.ui.pyside.utils.widgets import ItemFrame


class SellerWidget(ItemFrame):
    __seller_id: int
    __name: str
    __active: bool

    __selected: bool

    def __init__(self, seller_pd: ViewSeller, parent=None):
        super().__init__()
        self.__parent = parent

        self.ui = UI_SellerWidget()
        self.ui.setup_ui(self)

        self.seller_id = seller_pd.seller_id
        self.name = seller_pd.name
        self.active = seller_pd.active

        self.set_default_style()
        self.ui.label_name.clicked.connect(self.on_clicked_name)
        self.ui.line_edit_name.editingFinished.connect(self.on_pressed_line_name)
        self.ui.line_edit_name.escaped.connect(self.on_escaped_line_name)
        self.ui.active_box.toggled.connect(self.on_changed_active)

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def __get_seller_id(self) -> int:
        return self.__seller_id

    def __sat_seller_id(self, seller_id: int) -> None:
        self.__seller_id = seller_id

    seller_id = property(__get_seller_id, __sat_seller_id)

    def __get_name(self) -> str:
        return self.__name

    def __sat_name(self, name: str) -> None:
        self.__name = name
        self.ui.label_name.setText(name)
        self.ui.line_edit_name.setText(name)

    name = property(__get_name, __sat_name)

    def __get_active(self) -> bool:
        return self.__active

    def __sat_active(self, active: bool) -> None:
        self.__active = active
        self.ui.active_box.setChecked(active)

    active = property(__get_active, __sat_active)

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def __get_selected(self) -> bool:
        return self.__selected

    def __set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.ui.label_name.hide()
            self.ui.line_edit_name.show()
            self.ui.line_edit_name.setFocus()
        else:
            self.ui.label_name.show()
            self.ui.line_edit_name.hide()

    selected = property(__get_selected, __set_selected)

    def on_clicked_name(self):
        if self.parent_widget:
            self.parent_widget.on_clicked_label_name(self.seller_id)
        else:
            self.selected = True

    def on_pressed_line_name(self):
        name_text = self.ui.line_edit_name.text().strip()
        if name_text == self.name:
            return None
        if self.parent_widget:
            self.parent_widget.on_edit_seller_name(self.seller_id, name_text)
        else:
            self.selected = False
            self.name = name_text

    def on_escaped_line_name(self):
        self.name = self.name
        self.selected = False

    def on_changed_active(self, state: bool):
        if self.parent_widget:
            self.parent_widget.on_changed_active(self.seller_id, state)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(480, 320)
    v_box = QVBoxLayout(win)
    pd_item = ViewSeller(seller_id=2, name='Igor', hidden=True)
    frame = SellerWidget(seller_pd=pd_item)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    v_box.addWidget(frame)
    v_box.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))
    win.show()
    sys.exit(app.exec())
