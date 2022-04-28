import datetime

from prjstore.ui.pyside.expenses_editor.components.ui_expense_widget import *
from prjstore.ui.pyside.expenses_editor.schemas import ViewExpense
from prjstore.ui.pyside.utils.format_price import format_price
from prjstore.ui.pyside.utils.widgets import SelectableItemFrame


class ExpenseWidget(SelectableItemFrame):
    __data: ViewExpense
    __selected: bool

    def __init__(self, expense_pd: ViewExpense, parent=None):
        super().__init__()
        self.__parent = parent

        self.ui = UI_ExpenseWidget()
        self.ui.setup_ui(self)
        self.__selected = False

        self.data = expense_pd

        self.ui.btn_del.clicked.connect(self.on_click_del)
        self.ui.btn_ok.clicked.connect(self.on_click_ok)

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def update_ui(self):
        self.ui.combo_box_place.clear()
        for place_id, place in self.__data.places.items():
            self.ui.combo_box_place.addItem(place, place_id)
        self.place_id = self.__data.place_id
        self.desc = self.__data.desc
        self.date_cost = self.__data.date_cost
        self.cost = self.__data.cost

    def __get_data(self) -> ViewExpense:
        return self.__data

    def __set_data(self, data: ViewExpense):
        self.__data = data
        self.update_ui()

    data = property(__get_data, __set_data)

    def get_form_data(self) -> ViewExpense:
        form = self.__data.copy()
        form.place_id = self.ui.combo_box_place.currentData()
        form.desc = self.ui.line_edit_desc.text()
        form.date_cost = self.ui.date_edit.date().toPython()
        form.cost = float(self.ui.line_edit_cost.text())
        return form

    def __get_expense_id(self) -> int:
        return self.__data.id

    expense_id = property(__get_expense_id)

    def __get_place_id(self) -> int:
        return self.__data.place_id

    def __sat_place_id(self, place_id: int) -> None:
        self.__data.place_id = place_id
        self.ui.label_place.setText(self.__data.places[place_id])
        index = self.ui.combo_box_place.findData(place_id)
        if index and index > 0:
            self.ui.combo_box_place.setCurrentIndex(index)
        else:
            self.ui.combo_box_place.setCurrentIndex(0)

    place_id = property(__get_place_id, __sat_place_id)

    def __get_desc(self) -> str:
        return self.__data.desc

    def __sat_desc(self, desc: str) -> None:
        self.__data.desc = desc
        self.ui.label_desc.setText(desc)
        self.ui.line_edit_desc.setText(desc)

    desc = property(__get_desc, __sat_desc)

    def __get_date_cost(self) -> datetime.date:
        return self.__data.date_cost

    def __sat_date_cost(self, date_cost: datetime.date) -> None:
        self.__data.date_cost = date_cost
        self.ui.label_date.setText(date_cost.strftime('%d.%m.%Y'))
        self.ui.date_edit.setDate(date_cost)

    date_cost = property(__get_date_cost, __sat_date_cost)

    def __get_cost(self) -> float:
        return self.__data.cost

    def __sat_cost(self, cost: float) -> None:
        self.__data.cost = cost
        self.ui.label_cost.setText(f'{format_price(cost, dot=True)}{self.__data.sign}')
        self.ui.line_edit_cost.setText(format_price(cost))

    cost = property(__get_cost, __sat_cost)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.parent_widget:
            self.parent_widget.selected_expense_id = self.expense_id
        else:
            self.selected = True
        return QFrame.mousePressEvent(self, event)

    def __get_selected(self) -> bool:
        return self.__selected

    def __set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.set_selected_style()
            self.update_ui()
            self.ui.label_place.hide()
            self.ui.combo_box_place.show()
            self.ui.label_desc.hide()
            self.ui.line_edit_desc.show()
            self.ui.label_date.hide()
            self.ui.date_edit.show()
            self.ui.label_cost.hide()
            self.ui.line_edit_cost.show()
            self.ui.btn_del.show()
            self.ui.btn_ok.show()
        else:
            self.set_default_style()
            self.ui.label_place.show()
            self.ui.combo_box_place.hide()
            self.ui.label_desc.show()
            self.ui.line_edit_desc.hide()
            self.ui.label_date.show()
            self.ui.date_edit.hide()
            self.ui.label_cost.show()
            self.ui.line_edit_cost.hide()
            self.ui.btn_del.hide()
            self.ui.btn_ok.hide()

    selected = property(__get_selected, __set_selected)

    def on_click_ok(self):
        if self.parent_widget:
            forma = self.get_form_data()
            if forma != self.__data:
                # data changed
                self.parent_widget.edit_expense(forma)
            else:
                self.selected = False
        else:
            print(self.get_form_data())

    def on_click_del(self):
        if self.parent_widget:
            self.parent_widget.delete_expense(self.expense_id)
        else:
            print('del')


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
