import datetime
import sys

from prjstore.db.schemas import handler_items_editor as db_schemas
from prjstore.handlers.items_editor_handler import ItemsEditorHandler
from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.items_editor import schemas
from prjstore.ui.pyside.items_editor import thread
from prjstore.ui.pyside.items_editor.components.item_widget import ItemWidget
from prjstore.ui.pyside.items_editor.ui_items_editor import UI_ItemsEditor, DelMessageBox
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout
from util.pages import Pages


class ItemsEditor(AbstractModule, QWidget, Pages):
    __handler: ItemsEditorHandler
    __pd_items: list[schemas.ViewItem]
    __selected_item_widget: ItemWidget

    def __init__(self, parent=None, user_data=None, dark_style=False):
        AbstractModule.__init__(self, parent)
        QWidget.__init__(self)
        self.__handler = None
        self.name = 'edit_items_form'
        self.observer_module_names = ['price_editor_form', 'sale_form']
        self.ui = UI_ItemsEditor()
        self.ui.setup_ui(self)

        Pages.__init__(self)
        self.register_observer(self.ui.pages_frame)

        self.thread_pool = QThreadPool()

        if dark_style:
            self.setup_dark_style()
        self.__selected_item_widget = None
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.ui.src_items.textChanged.connect(self.on_search_text_changed)

        if parent:
            if parent.dark_style:
                self.setup_dark_style()
            handler = ItemsEditorHandler(main_handler=parent.handler)
            self.__connected_complete(handler)
        else:
            db_connector = thread.DbConnect(user_data)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.__connected_complete)
            self.thread_pool.start(db_connector)

    def get_selected_item_widget(self) -> ItemWidget:
        return self.__selected_item_widget

    def set_selected_item_widget(self, selected_item_widget: ItemWidget) -> None:
        if selected_item_widget is not self.selected_item_widget:
            if self.selected_item_widget:
                self.selected_item_widget.selected = False
            self.__selected_item_widget = selected_item_widget
            if selected_item_widget.sale_details is None:
                db_get_sales = thread.DBGetSales(self.handler, selected_item_widget.item_id)
                db_get_sales.signals.error.connect(self.__connection_error)
                db_get_sales.signals.result.connect(self._completed_getting_sales)
                self.thread_pool.start(db_get_sales)
            else:
                selected_item_widget.selected = True
        else:
            del self.selected_item_widget

    def _completed_getting_sales(self, sales: list[db_schemas.SaleDetail]):
        self.selected_item_widget.sale_details = sales
        self.selected_item_widget.selected = True

    def del_selected_item_widget(self) -> None:
        self.__selected_item_widget.selected = False
        self.__selected_item_widget = None

    selected_item_widget = property(get_selected_item_widget, set_selected_item_widget, del_selected_item_widget)

    def setup_dark_style(self):
        self.setStyleSheet(
            '#ItemsEditor, #ItemsFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            '#LineEditStcItems {background-color: #121212; color: #dcdcdc;}\n'
        )

    def on_search_text_changed(self):
        self.load_widget.show()
        self.selected_page = 1
        self.update_ui()
        self.load_widget.hide()

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: ItemsEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self):
        if self.need_update:
            self.load_widget.show()
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self, updating_data: bool = True):
        if updating_data:
            self.__pd_items = self.handler.get_store_items(search=self.ui.src_items.text())
            self.count_elements = len(self.__pd_items)
        clearLayout(self.ui.layout_items)
        self.__selected_item_widget = None
        for i in self.items_on_page:
            item_frame = ItemWidget(item_pd=self.__pd_items[i], parent=self)
            self.ui.layout_items.addWidget(item_frame)

    def page_number_changed(self, data_page):
        if data_page:
            self.update_ui(updating_data=False)

    def on_press_edit_item(self, selected_item_widget: ItemWidget) -> None:
        item_id = selected_item_widget.item_id
        qty = selected_item_widget.ui.qty_box.text()
        price = selected_item_widget.ui.line_edit_price_buy.text()
        pd_data = db_schemas.ItemFormEdit(id=item_id, new_qty=qty, new_price=price)
        self.load_widget.show()
        db_edit_item = thread.DBEditItem(self.handler, pd_data)
        db_edit_item.signals.error.connect(self.__connection_error)
        db_edit_item.signals.result.connect(self.__update_item_complete)
        self.thread_pool.start(db_edit_item)

    def __update_item_complete(self, data: db_schemas.ItemFormEdit):
        self.selected_item_widget.qty = data.new_qty
        self.selected_item_widget.price_buy = data.new_price
        del self.selected_item_widget
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def on_press_del_item(self, selected_item_widget: ItemWidget) -> None:
        result = DelMessageBox(self).exec()
        if result == QMessageBox.Yes:
            item_id = selected_item_widget.item_id
            self.load_widget.show()
            db_edit_product = thread.DBDeleteItem(self.handler, item_id)
            db_edit_product.signals.error.connect(self.__connection_error)
            db_edit_product.signals.complete.connect(self.__deleted_item_complete)
            self.thread_pool.start(db_edit_product)

    def __deleted_item_complete(self):
        if self.parent:
            self.parent.data_changed(self)
        self.update_ui()
        self.load_widget.hide()

    def on_click_item_sale(self, date: datetime.date):
        if self.parent:
            self.parent.on_click_item_sale(date)


if __name__ == "__main__":
    from prjstore.db.api import settings

    app = QApplication(sys.argv)
    w = ItemsEditor(user_data=settings.user_data, dark_style=True)
    w.show()
    sys.exit(app.exec())
