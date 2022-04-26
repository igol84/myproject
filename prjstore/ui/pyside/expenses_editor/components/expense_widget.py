import datetime

from prjstore.ui.pyside.expenses_editor.components.ui_expense_widget import *
from prjstore.ui.pyside.expenses_editor.schemas import ViewExpense
from prjstore.ui.pyside.utils.format_price import format_price
from prjstore.ui.pyside.utils.widgets import ItemFrame


class ExpenseWidget(ItemFrame):
    __expense_id: int
    __places: dict[int, str]
    __place_id: int
    __desc: str
    __date_cost: datetime.date
    __cost: float
    __sign: str = '₴'

    __selected: bool

    def __init__(self, expense_pd: ViewExpense, parent=None):
        super().__init__()
        self.__parent = parent

        self.ui = UI_ExpenseWidget()
        self.ui.setup_ui(self)
        self.__selected = False

        self.set_default_style()
        self.update_ui(expense_pd)

    def enterEvent(self, event):
        if not self.selected:
            self.set_hover_style()

    def leaveEvent(self, event):
        if not self.selected:
            self.set_default_style()

    def set_default_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.default_color_bg}; color: {self.default_color_text};')

    def set_hover_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.color_fon_on_enter}; color: {self.default_color_text};')

    def set_selected_style(self) -> None:
        self.setStyleSheet(f'background-color: {self.current_color_bg}; color: {self.current_color_text}')

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def update_ui(self, expense_pd: ViewExpense):
        self.__places = expense_pd.places
        for place_id, place in expense_pd.places.items():
            self.ui.combo_box_place.addItem(place, place_id)
        self.__expense_id = expense_pd.id
        self.place_id = expense_pd.place_id
        self.desc = expense_pd.desc
        self.date_cost = expense_pd.date_cost
        self.cost = expense_pd.cost

    def __get_expense_id(self) -> int:
        return self.__expense_id

    expense_id = property(__get_expense_id)

    def __get_place_id(self) -> int:
        return self.__place_id

    def __sat_place_id(self, place_id: int) -> None:
        self.__place_id = place_id
        self.ui.label_place.setText(self.__places[place_id])
        index = self.ui.combo_box_place.findData(place_id)
        if index and index > 0:
            self.ui.combo_box_place.setCurrentIndex(index)
        else:
            self.ui.combo_box_place.setCurrentIndex(0)

    place_id = property(__get_place_id, __sat_place_id)

    def __get_desc(self) -> str:
        return self.__desc

    def __sat_desc(self, desc: str) -> None:
        self.__desc = desc
        self.ui.label_desc.setText(desc)
        self.ui.line_edit_desc.setText(desc)

    desc = property(__get_desc, __sat_desc)

    def __get_date_cost(self) -> datetime.date:
        return self.__date_cost

    def __sat_date_cost(self, date_cost: datetime.date) -> None:
        self.__date_cost = date_cost
        self.ui.label_date.setText(date_cost.strftime('%d.%m.%Y'))
        self.ui.date_edit.setDate(date_cost)

    date_cost = property(__get_date_cost, __sat_date_cost)

    def __get_cost(self) -> float:
        return self.__cost

    def __sat_cost(self, cost: float) -> None:
        self.__cost = cost
        self.ui.label_cost.setText(f'{format_price(cost, dot=True)}{self.__sign}')
        self.ui.line_edit_cost.setText(f'{cost}')

    cost = property(__get_cost, __sat_cost)

    def __get_selected(self) -> bool:
        return self.__selected

    def __set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.ui.label_place.hide()
            self.ui.combo_box_place.show()
            self.ui.label_desc.hide()
            self.ui.line_edit_desc.show()
            self.ui.label_date.hide()
            self.ui.date_edit.show()
            self.ui.label_cost.hide()
            self.ui.line_edit_cost.show()
        else:
            self.ui.label_place.show()
            self.ui.combo_box_place.hide()
            self.ui.label_desc.show()
            self.ui.line_edit_desc.hide()
            self.ui.label_date.show()
            self.ui.date_edit.hide()
            self.ui.label_cost.show()
            self.ui.line_edit_cost.hide()

    selected = property(__get_selected, __set_selected)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(480, 320)
    v_box = QVBoxLayout(win)
    places = {1: 'internet', 2: 'box'}
    pd_item = ViewExpense(id=1, places=places, place_id=1, desc='prom', date_cost=datetime.date.today(), cost=1500)
    frame = ExpenseWidget(expense_pd=pd_item)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    v_box.addWidget(frame)
    v_box.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))
    win.show()
    sys.exit(app.exec())
