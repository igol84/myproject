import datetime

from prjstore.ui.pyside.items_editor.components.ui_item_widget import *
from prjstore.ui.pyside.items_editor.schemas import ViewItem
from prjstore.ui.pyside.utils.format_price import format_price
from prjstore.ui.pyside.utils.widgets import ItemFrame


class ItemWidget(ItemFrame):
    __item_id: int
    __desc: str
    __price_buy: float
    __sign: str
    __qty: int
    __date_buy: datetime.date
    __dates_of_sale: list[datetime.date]

    __parent: object
    __selected: bool

    def __init__(self, item_pd: ViewItem, parent=None):
        super().__init__()
        self.__parent = parent
        self.__selected = False
        self.__sign = item_pd.sign
        self.ui = UI_ItemWidget()
        self.ui.setup_ui(self)
        self.item_id = item_pd.item_id
        self.desc = item_pd.desc
        self.price_buy = item_pd.price_buy
        self.qty = item_pd.qty
        self.date_buy = item_pd.date_buy
        self.__dates_of_sale = item_pd.dates_of_sale
        self.set_default_style()

    def get_parent(self):
        return self.__parent

    parent_widget = property(get_parent)

    def get_item_id(self) -> int:
        return self.__item_id

    def sat_item_id(self, item_id: int) -> None:
        self.__item_id = item_id
        self.ui.label_prod_id.setText(str(item_id))

    item_id = property(get_item_id, sat_item_id)

    def get_desc(self) -> str:
        return self.__desc

    def sat_desc(self, desc: str) -> None:
        self.__desc = desc
        self.ui.label_desc.setText(desc)

    desc = property(get_desc, sat_desc)

    def get_price_buy(self) -> float:
        return self.__price_buy

    def sat_price_buy(self, price_buy: float) -> None:
        self.__price_buy = price_buy
        self.ui.label_price_buy.setText(self.get_price_format())
        self.ui.line_edit_price_buy.setText(format_price(price_buy))

    price_buy = property(get_price_buy, sat_price_buy)

    def get_price_format(self) -> str:
        return f'{format_price(self.price_buy, dot=True)}{self.__sign}'

    def get_qty(self) -> int:
        return self.__qty

    def sat_qty(self, qty: int) -> None:
        self.__qty = qty
        self.ui.label_qty.setText(f'{qty:,}шт.')
        self.ui.qty_box.setValue(qty)

    qty = property(get_qty, sat_qty)

    def get_date_buy(self) -> str:
        return self.__date_buy

    def sat_date_buy(self, date_buy: str) -> None:
        self.__date_buy = date_buy
        self.ui.label_date_buy.setText(date_buy)

    date_buy = property(get_date_buy, sat_date_buy)

    def get_selected(self) -> bool:
        return self.__selected

    def set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.set_selected_style()
            self.ui.button.show()
            self.ui.empty_button.hide()
            self.ui.qty_box.show()
            self.ui.label_qty.hide()
            self.ui.line_edit_price_buy.show()
            self.ui.label_price_buy.hide()
        else:
            self.set_default_style()
            self.ui.button.hide()
            self.ui.empty_button.show()
            self.ui.qty_box.hide()
            self.ui.label_qty.show()
            self.ui.line_edit_price_buy.hide()
            self.ui.label_price_buy.show()

    selected = property(get_selected, set_selected)

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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.parent_widget:
            self.parent_widget.selected_item_widget = self
        else:
            self.selected = True
        return QFrame.mousePressEvent(self, event)


if __name__ == '__main__':
    pd_item = ViewItem(item_id=5, desc='shoes nike 24 shoes nike 24 shoes nike 24 shoes nike 24', price_buy=2400.5,
                       qty=20000, date_buy='24.05.2021')
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ItemWidget(item_pd=pd_item)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
