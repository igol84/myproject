import datetime
from typing import Optional

from prjstore.ui.pyside.expenses_editor.components.ui_add_expense_widget import *
from prjstore.ui.pyside.expenses_editor import schemas
from prjstore.ui.pyside.utils.is_digit import is_digit
from prjstore.ui.pyside.utils.widgets import ItemFrame


class AddExpenseWidget(ItemFrame):

    def __init__(self, parent=None, view_data: schemas.ViewNewExpense = None):
        super().__init__()
        self.__parent = parent

        self.ui = UI_AddExpenseWidget()
        self.ui.setup_ui(self)
        if view_data:
            self.setup_combo_box_places(view_data.places)
        self.ui.date_edit.setDate(view_data.date)

        self.set_default_style()
        self.ui.btn_add.clicked.connect(self.on_push_btn)

    def setup_combo_box_places(self, date: dict[int, str]):
        self.ui.combo_box_places.clear()
        self.ui.combo_box_places.addItem('')
        for place_id, place in date.items():
            self.ui.combo_box_places.addItem(place, place_id)

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def get_date(self) -> schemas.FormNewExpense:
        date = schemas.FormNewExpense(place_id=self.place_id, desc=self.desc, date_cost=self.date_cost, cost=self.cost)
        return date

    def on_push_btn(self) -> None:
        date = self.get_date()
        if date and self.parent_widget:
            self.parent_widget.on_add_expense(date)

    def __get_place_id(self) -> Optional[int]:
        if self.ui.combo_box_places.currentData():
            return int(self.ui.combo_box_places.currentData())

    place_id = property(__get_place_id)

    def __get_desc(self) -> str:
        return self.ui.line_edit_desc.text()

    desc = property(__get_desc)

    def __get_date_cost(self) -> datetime.date:
        return self.ui.date_edit.date().toPython()

    date_cost = property(__get_date_cost)

    def __get_cost(self) -> Optional[float]:
        if is_digit(cost := self.ui.line_edit_cost.text()):
            return float(cost)

    cost = property(__get_cost)

    def clear_form(self):
        self.ui.combo_box_places.setCurrentIndex(0)
        self.ui.line_edit_desc.setText('')
        self.ui.date_edit.setDate(datetime.date.today())
        self.ui.line_edit_cost.setText('')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(580, 320)
    v_box = QVBoxLayout(win)
    data = schemas.ViewNewExpense(places={1: 'internet', 2: 'box'})
    frame = AddExpenseWidget(view_data=data)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    v_box.addWidget(frame)
    v_box.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))
    win.show()
    sys.exit(app.exec())
