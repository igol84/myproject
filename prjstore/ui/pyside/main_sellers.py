import sys
from typing import Optional

from prjstore.handlers.sellers_editor_handler import SellersEditorHandler
from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.sellers_editor import schemas
from prjstore.ui.pyside.sellers_editor import thread
from prjstore.ui.pyside.sellers_editor.components.add_seller_widget import AddSellerWidget
from prjstore.ui.pyside.sellers_editor.components.seller_widget import SellerWidget
from prjstore.ui.pyside.sellers_editor.ui_sellers_editor import UI_SellersEditor
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class SellersEditor(QWidget, ObserverInterface):
    __pd_sellers: list[schemas.ViewSeller]
    __selected_seller_id: Optional[int]
    __seller_widgets: dict[int, SellerWidget]
    __handler: SellersEditorHandler
    __dark_style: bool

    def __init__(self, parent=None, test=False, user_data=None, list_pd_sellers=None, db=None, dark_style=False):
        super().__init__()
        self.parent: MainWindowInterface = parent
        if parent:
            self.parent.register_observer(self)
        self.__handler = None
        self.test = test
        self.ui = UI_SellersEditor()
        self.ui.setup_ui(self)
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.dark_style = dark_style
        if list_pd_sellers is None:
            list_pd_sellers = []
        self.list_pd_sellers: list = list_pd_sellers
        self.__selected_seller_id = None
        self.__seller_widgets = {}
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.parent:
            if not self.test:
                db_connector = thread.DbConnect(self.user_data, self.db)
                db_connector.signals.error.connect(self.__connection_error)
                db_connector.signals.result.connect(self.__connected_complete)
                self.thread_pool.start(db_connector)
            else:
                self.__connected_complete(SellersEditorHandler(db=None, test=True))
        else:
            store = self.parent.handler.store
            self.__connected_complete(SellersEditorHandler(db=self.db, store=store))

    def get_selected_seller_id(self) -> int:
        return self.__selected_seller_id

    def set_selected_seller_id(self, selected_seller_id: Optional[int]) -> None:
        if self.selected_seller_id:
            self.selected_widget.selected = False
        if selected_seller_id is not None:
            self.__selected_seller_id = selected_seller_id
            self.selected_widget.selected = True
        else:
            self.__selected_seller_id = None

    selected_seller_id = property(get_selected_seller_id, set_selected_seller_id)

    def get_selected_widget(self) -> SellerWidget:
        if self.selected_seller_id:
            return self.__seller_widgets[self.selected_seller_id]

    selected_widget = property(get_selected_widget)

    def get_dark_style(self) -> bool:
        return self.__dark_style

    def set_dark_style(self, flag: bool) -> None:
        self.__dark_style = flag
        if flag:
            self.setStyleSheet(
                '#SellersEditor, #SellersFrame {background-color: #2F303B; color: #F8F8F2;}\n'
                'QLabel {color: #F8F8F2;}\n'
            )

    dark_style = property(get_dark_style, set_dark_style)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: SellersEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self, store=None) -> None:
        self.load_widget.show()
        self.handler.update_data(store)
        self.update_ui()
        self.load_widget.hide()

    def update_ui(self) -> None:
        clearLayout(self.ui.layout_sellers)
        self.__pd_sellers = self.handler.get_store_sellers()
        self.ui.layout_sellers.addWidget(AddSellerWidget(self))
        for pd_seller in self.__pd_sellers:
            item_frame = SellerWidget(pd_seller, self)
            self.__seller_widgets[pd_seller.seller_id] = item_frame
            self.ui.layout_sellers.addWidget(item_frame)
        if self.selected_seller_id:
            self.set_selected_seller_id(self.selected_seller_id)

    def on_clicked_label_name(self, seller_id: int) -> None:
        self.selected_seller_id = seller_id

    def on_edit_seller_name(self, seller_id: int, new_name: str):
        self.load_widget.show()
        db_seller = thread.DBEditSellerName(self.handler, seller_id, new_name)
        db_seller.signals.error.connect(self.__connection_error)
        db_seller.signals.result.connect(self.__update_seller_name_complete)
        self.thread_pool.start(db_seller)

    def __update_seller_name_complete(self, seller_id: int, new_name: str):
        self.__seller_widgets[seller_id].name = new_name
        self.__seller_widgets[seller_id].selected = False
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def on_changed_active(self, seller_id: int, active: bool):
        self.load_widget.show()
        db_seller = thread.DBEditSellerActive(self.handler, seller_id, active)
        db_seller.signals.error.connect(self.__connection_error)
        db_seller.signals.compleate.connect(self.__update_seller_active_complete)
        self.thread_pool.start(db_seller)

    def __update_seller_active_complete(self):
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def on_add_seller(self, name: str):
        self.load_widget.show()
        db_seller = thread.DBAddSeller(self.handler, name)
        db_seller.signals.error.connect(self.__connection_error)
        db_seller.signals.result.connect(self.__adding_seller_complete)
        self.thread_pool.start(db_seller)

    def __adding_seller_complete(self, pd_new_seller: schemas.ViewSeller):
        item_frame = SellerWidget(pd_new_seller, self)
        self.__seller_widgets[pd_new_seller.seller_id] = item_frame
        self.ui.layout_sellers.insertWidget(1, item_frame)
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SellersEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
