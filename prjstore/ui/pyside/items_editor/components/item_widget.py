from prjstore.db.schemas import handler_items_editor as db_schemas
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
    __sale_details: list[db_schemas.SaleDetail]

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
        self.sale_details = item_pd.dates_of_sale
        self.set_default_style()
        self.ui.button_edit.clicked.connect(self.on_clicked_edit)
        self.ui.button_del.clicked.connect(self.on_clicked_del)
        self.ui.list_sales.clicked.connect(self.on_clicked_sale)

    def __get_parent(self):
        return self.__parent

    parent_widget = property(__get_parent)

    def __get_item_id(self) -> int:
        return self.__item_id

    def __sat_item_id(self, item_id: int) -> None:
        self.__item_id = item_id
        self.ui.label_prod_id.setText(str(item_id))

    item_id = property(__get_item_id, __sat_item_id)

    def __get_desc(self) -> str:
        return self.__desc

    def __sat_desc(self, desc: str) -> None:
        self.__desc = desc
        self.ui.label_desc.setText(desc)

    desc = property(__get_desc, __sat_desc)

    def __get_price_buy(self) -> float:
        return self.__price_buy

    def __sat_price_buy(self, price_buy: float) -> None:
        self.__price_buy = price_buy
        self.ui.label_price_buy.setText(self.get_price_format())
        self.ui.line_edit_price_buy.setText(format_price(price_buy))

    price_buy = property(__get_price_buy, __sat_price_buy)

    def get_price_format(self) -> str:
        return f'{format_price(self.price_buy, dot=True)}{self.__sign}'

    def __get_qty(self) -> int:
        return self.__qty

    def __sat_qty(self, qty: int) -> None:
        self.__qty = qty
        self.ui.label_qty.setText(f'{qty:,}шт.')
        self.ui.qty_box.setValue(qty)

    qty = property(__get_qty, __sat_qty)

    def __get_date_buy(self) -> datetime.date:
        return self.__date_buy

    def __sat_date_buy(self, date_buy: datetime.date) -> None:
        self.__date_buy = date_buy
        text = date_buy.strftime("%d-%m-%Y")
        self.ui.label_date_buy.setText(text)

    date_buy = property(__get_date_buy, __sat_date_buy)

    def __get_sale_details(self) -> list[db_schemas.SaleDetail]:
        return self.__sale_details

    def __set_sale_details(self, dales_detail: list[db_schemas.SaleDetail]) -> None:
        self.ui.list_sales.clear()
        self.__sale_details = dales_detail
        if dales_detail is not None:
            for sale_detail in dales_detail:
                text = sale_detail.get_text(self.__sign)
                self.ui.list_sales.addItem(WidgetItem(text=text, date=sale_detail.date))

    sale_details = property(__get_sale_details, __set_sale_details)

    def __get_selected(self) -> bool:
        return self.__selected

    def __set_selected(self, flag: bool = True) -> None:
        self.__selected = flag
        if flag:
            self.set_selected_style()
            self.ui.qty_box.show()
            self.ui.label_qty.hide()
            self.ui.line_edit_price_buy.show()
            self.ui.label_price_buy.hide()
            self.ui.empty_button.hide()
            self.ui.button_edit.show()
            self.ui.button_del.show()
            self.ui.list_sales.show()
        else:
            self.set_default_style()
            self.ui.qty_box.hide()
            self.ui.label_qty.show()
            self.ui.line_edit_price_buy.hide()
            self.ui.label_price_buy.show()
            self.ui.empty_button.show()
            self.ui.button_edit.hide()
            self.ui.button_del.hide()
            self.ui.list_sales.hide()

    selected = property(__get_selected, __set_selected)

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

    def on_clicked_edit(self):
        if self.parent_widget:
            self.parent_widget.on_press_edit_item(self)
        else:
            self.selected = False

    def on_clicked_del(self):
        if self.parent_widget:
            self.parent_widget.on_press_del_item(self)
        else:
            self.selected = False

    # TODO
    def on_clicked_sale(self, item: QListWidgetItem):
        if self.parent_widget:
            print(item.data(Qt.UserRole))


if __name__ == '__main__':
    pd_item = ViewItem(item_id=5, desc='shoes nike 24 shoes nike 24 shoes nike 24 shoes nike 24', price_buy=2400.5,
                       qty=20000, date_buy=datetime.datetime(2020, 5, 17).date())
    import sys

    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(480, 320)
    v_box = QVBoxLayout(win)
    frame = ItemWidget(item_pd=pd_item)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    v_box.addWidget(frame)
    v_box.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))
    win.show()
    sys.exit(app.exec())
