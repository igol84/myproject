import sys

from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.product_price_editor.components import FrameProductFactory
from prjstore.ui.pyside.product_price_editor.components.abstract_product import AbstractItem
from prjstore.ui.pyside.product_price_editor.schemas import *
from prjstore.ui.pyside.product_price_editor.thread import *
from prjstore.ui.pyside.product_price_editor.ui_product_price_edit import UI_Frame
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *


class SaleForm(QWidget):
    products: list[ModelProduct]
    selected_item_widget: AbstractItem
    handler: ProductPriceEditor

    def __init__(self, parent=None, test=False, user_data=None, list_pd_product=None, db=None):
        super().__init__()
        self.parent: MainWindowInterface = parent
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.test = test
        if list_pd_product is None:
            list_pd_product = []
        self.list_pd_prod: list = list_pd_product
        self.resize(500, 600)
        self.ui = UI_Frame()
        self.ui.setup_ui(self)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.test:
            db_connector = DbConnect(self.user_data, self.db)
            db_connector.signals.error.connect(self._connection_error)
            db_connector.signals.result.connect(self.connected_complete)
            self.thread_pool.start(db_connector)

    def _connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def connected_complete(self, handler: ProductPriceEditor):
        self.handler = handler
        self.products = self.handler.get_store_products()

        self.update()
        self.load_widget.hide()

    def update(self):
        self._update_items_layout()

    def _update_items_layout(self):
        self.selected_item_widget = None
        self.layout = QVBoxLayout()
        for item in self.products:
            item_frame = FrameProductFactory.create(product_type=item.type, parent=self, item_pd=item)
            self.layout.addWidget(item_frame)
        self.ui.product_frame.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm(test=False, user_data={'username': 'qwe', 'password': 'qwe'})
    w.show()
    sys.exit(app.exec())
