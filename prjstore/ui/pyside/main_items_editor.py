import sys

from prjstore.handlers.items_editor_handler import ItemsEditorHandler
from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.items_editor import schemas
from prjstore.ui.pyside.items_editor.components.item_widget import ItemWidget
from prjstore.ui.pyside.items_editor.thread import DbConnect
from prjstore.ui.pyside.items_editor.ui_main_items_editor import UI_ItemsEditor
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

        if not self.parent:
            if not self.test:
                db_connector = DbConnect(self.user_data, self.db)
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
        if selected_item_widget is not self.__selected_item_widget:
            selected_item_widget.selected = True
            if self.__selected_item_widget:
                self.__selected_item_widget.selected = False
            self.__selected_item_widget = selected_item_widget
        else:
            del self.selected_item_widget

    def del_set_selected_item_widget(self) -> None:
        self.__selected_item_widget.selected = False
        self.__selected_item_widget = None

    selected_item_widget = property(get_selected_item_widget, set_selected_item_widget, del_set_selected_item_widget)

    def setup_dark_style(self):
        self.setStyleSheet(
            ''
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ItemsEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
