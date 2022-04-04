import sys

from prjstore.db.schemas import handler_items_editor as db_schemas
from prjstore.handlers.items_editor_handler import ItemsEditorHandler
from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.items_editor import schemas
from prjstore.ui.pyside.items_editor.components.item_widget import ItemWidget
from prjstore.ui.pyside.items_editor import thread
from prjstore.ui.pyside.items_editor.ui_items_editor import UI_ItemsEditor, DelMessageBox
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class ItemsEditor(QWidget, ObserverInterface):
    __pd_items: list[schemas.ViewItem]
    __selected_item_widget: ItemWidget
    __handler: ItemsEditorHandler

    def __init__(self, parent=None, test=False, user_data=None, list_pd_items=None, db=None, dark_style=False):
        super().__init__()
        self.parent: MainWindowInterface = parent
        if parent:
            self.parent.register_observer(self)
        self.__handler = None
        self.test = test
        self.ui = UI_ItemsEditor()
        self.ui.setup_ui(self)
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.dark_style = dark_style
        if list_pd_items is None:
            list_pd_items = []
        self.list_pd_items: list = list_pd_items

        if self.dark_style:
            self.setup_dark_style()
        self.__selected_item_widget = None
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.ui.src_items.textChanged.connect(self.on_search_text_changed)

        if not self.parent:
            if not self.test:
                db_connector = thread.DbConnect(self.user_data, self.db)
                db_connector.signals.error.connect(self.__connection_error)
                db_connector.signals.result.connect(self.__connected_complete)
                self.thread_pool.start(db_connector)
            else:
                self.__connected_complete(ItemsEditorHandler(db=None, test=True))
        else:
            store = self.parent.handler.store
            handler = ItemsEditorHandler(db=self.db, store=store)
            self.__connected_complete(handler)

    def get_selected_item_widget(self) -> ItemWidget:
        return self.__selected_item_widget

    def set_selected_item_widget(self, selected_item_widget: ItemWidget) -> None:
        if selected_item_widget is not self.selected_item_widget:
            selected_item_widget.selected = True
            if self.selected_item_widget:
                self.selected_item_widget.selected = False
            self.__selected_item_widget = selected_item_widget
            if selected_item_widget.sale_details is None:
                self.load_widget.show()
                db_get_sales = thread.DBGetSales(self.handler, selected_item_widget.item_id)
                db_get_sales.signals.error.connect(self.__connection_error)
                db_get_sales.signals.result.connect(self._completed_getting_sales)
                self.thread_pool.start(db_get_sales)
        else:
            del self.selected_item_widget

    def _completed_getting_sales(self, sales: list[db_schemas.SaleDetail]):
        self.selected_item_widget.sale_details = sales
        self.load_widget.hide()

    def del_selected_item_widget(self) -> None:
        self.__selected_item_widget.selected = False
        self.__selected_item_widget = None

    selected_item_widget = property(get_selected_item_widget, set_selected_item_widget, del_selected_item_widget)

    def setup_dark_style(self):
        self.setStyleSheet(
            '#ItemsEditor, #ItemsFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            'QLineEdit {background-color: #121212; color: #dcdcdc;}\n'
            'QMessageBox {background-color: #121212; color: #dcdcdc;}'
        )

    def on_search_text_changed(self):
        self.load_widget.show()
        self.update_ui()
        self.load_widget.hide()

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: ItemsEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self, store=None):
        self.load_widget.show()
        self.handler.update_data(store)
        self.update_ui()
        self.load_widget.hide()

    def update_ui(self):
        self.__pd_items = self.handler.get_store_items(search=self.ui.src_items.text())
        clearLayout(self.ui.layout_items)
        self.__selected_item_widget = None
        for pd_item in self.__pd_items:
            item_frame = ItemWidget(item_pd=pd_item, parent=self)
            self.ui.layout_items.addWidget(item_frame)

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
        self.selected_item_widget.hide()
        del self.selected_item_widget
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ItemsEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
