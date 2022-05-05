import sys
from typing import Optional

from prjstore.db.api import settings
from prjstore.handlers.sellers_editor_handler import SellersEditorHandler
from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.sellers_editor import schemas
from prjstore.ui.pyside.sellers_editor import thread
from prjstore.ui.pyside.sellers_editor.components.add_seller_widget import AddSellerWidget
from prjstore.ui.pyside.sellers_editor.components.seller_widget import SellerWidget
from prjstore.ui.pyside.sellers_editor.ui_sellers_editor import UI_SellersEditor
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout
from util.pages import Pages


class SellersEditor(AbstractModule, QWidget, Pages):
    __handler: SellersEditorHandler
    __parent: MainWindowInterface
    __pd_sellers: list[schemas.ViewSeller]
    __selected_seller_id: Optional[int]
    __seller_widgets: dict[int, SellerWidget]
    __dark_style: bool

    def __init__(self, parent=None, user_data=None, dark_style=False):
        AbstractModule.__init__(self, parent)
        QWidget.__init__(self)
        self.name = 'sellers_form'
        self.observer_module_names = ['sale_form']
        self.__handler = None
        self.ui = UI_SellersEditor()
        self.ui.setup_ui(self)

        Pages.__init__(self, count_elements_on_page=13)
        self.register_observer(self.ui.pages_frame)

        self.thread_pool = QThreadPool()
        self.__selected_seller_id = None
        self.__seller_widgets = {}
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        if dark_style:
            self.setup_dark_style()
        if parent:
            if parent.dark_style:
                self.setup_dark_style()
            self.__connected_complete(SellersEditorHandler(main_handler=self.parent.handler))
        else:
            db_connector = thread.DbConnect(user_data)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.__connected_complete)
            self.thread_pool.start(db_connector)

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

    def setup_dark_style(self) -> None:
        self.setStyleSheet(
            '#SellersEditor, #SellersFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
        )

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: SellersEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self) -> None:
        if self.need_update:
            self.load_widget.show()
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self, updating_data: bool = True) -> None:
        clearLayout(self.ui.layout_sellers)
        if updating_data:
            self.__pd_sellers = self.handler.get_store_sellers()
            self.count_elements = len(self.__pd_sellers)
        self.ui.layout_sellers.addWidget(AddSellerWidget(self))
        for i in self.items_on_page:
            item_frame = SellerWidget(self.__pd_sellers[i], self)
            self.__seller_widgets[self.__pd_sellers[i].seller_id] = item_frame
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
        db_seller.signals.complete.connect(self.__adding_seller_complete)
        self.thread_pool.start(db_seller)

    def __adding_seller_complete(self):
        self.update_ui()
        self.selected_page = 1
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def page_number_changed(self, data_page):
        if data_page:
            self.update_ui(updating_data=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SellersEditor(user_data=settings.user_data, dark_style=True)
    w.show()
    sys.exit(app.exec())
