import sys

from prjstore.db.schemas.handler_product_price_editor import ModelShoes, ModelColor
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.product_price_editor import schemas
from prjstore.ui.pyside.product_price_editor.components import FrameProductFactory, ShoesFrame
from prjstore.ui.pyside.product_price_editor.components.abstract_product import AbstractItem
from prjstore.ui.pyside.product_price_editor.components.shoes_comps import SizeFrame, ColorFrame
from prjstore.ui.pyside.product_price_editor.thread import *
from prjstore.ui.pyside.product_price_editor.ui_product_price_edit import UI_Frame
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *


class SaleForm(QWidget):
    products: list[schemas.ModelProduct]
    selected_item_widget: AbstractItem
    handler: ProductPriceEditorHandler

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
        self.selected_shoes_frame: ShoesFrame = None
        self.selected_color_frame: ColorFrame = None
        self.selected_size_frame: SizeFrame = None
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.test:
            db_connector = DbConnect(self.user_data, self.db)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.connected_complete)
            self.thread_pool.start(db_connector)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def connected_complete(self, handler: ProductPriceEditorHandler):
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

    def on_press_edit_by_name(self, shoes_frame: ShoesFrame):
        self.selected_shoes_frame = shoes_frame
        name = shoes_frame.pr_name
        new_price = shoes_frame.desc_frame.price_line_edit.text()
        new_price = new_price if new_price else None
        new_name = shoes_frame.desc_frame.line_edit_desc.text()
        ps_shoes = ModelShoes(name=name, new_name=new_name, price_for_sale=new_price)
        self.load_widget.show()
        db_edit_shoes = DBEditShoes(self.handler, ps_shoes)
        db_edit_shoes.signals.error.connect(self.__connection_error)
        db_edit_shoes.signals.result.connect(self.__update_shoes_complete)
        self.thread_pool.start(db_edit_shoes)

    def __update_shoes_complete(self, pd_shoes: ModelShoes):
        self.selected_shoes_frame.desc_frame.set_selected(False)
        if pd_shoes.price_for_sale is not None:
            self.selected_shoes_frame.set_price_of_all_sizes(pd_shoes.price_for_sale)
        if pd_shoes.new_name is not None:
            self.selected_shoes_frame.set_new_name(pd_shoes.new_name)
        if self.selected_shoes_frame.selected_size_frame:
            self.selected_shoes_frame.selected_size_frame.set_selected(False)
        self.load_widget.hide()

    def on_color_edit(self, pr_name:str, color_frame: ColorFrame):
        self.selected_color_frame = color_frame
        color = color_frame.color
        new_color = color_frame.header.line_edit_color.text()
        price = color_frame.header.line_edit_price.text()
        price = price if price else None
        ps_color = ModelColor(name=pr_name, color=color, new_color=new_color, price_for_sale=price)
        self.load_widget.show()
        db_edit_color = DBEditColor(self.handler, ps_color)
        db_edit_color.signals.error.connect(self.__connection_error)
        db_edit_color.signals.result.connect(self.__update_color_complete)
        self.thread_pool.start(db_edit_color)

    def __update_color_complete(self, pd_color: ModelColor):
        self.selected_color_frame.color = pd_color.new_color
        if pd_color.price_for_sale is not None:
            self.selected_color_frame.set_price_of_all_sizes(pd_color.price_for_sale)
        self.load_widget.hide()

    def on_edit_size(self, size_frame: SizeFrame):
        self.selected_size_frame = size_frame
        pr_id = size_frame.pr_id
        size = size_frame.line_edit_size.text()
        price = size_frame.line_edit_price.text()
        pd_size = ModelProductForm(id=pr_id, size=size, price_for_sale=price)
        self.load_widget.show()
        db_edit_size = DBEditSize(self.handler, pd_size)
        db_edit_size.signals.error.connect(self.__connection_error)
        db_edit_size.signals.result.connect(self.__update_size_complete)
        self.thread_pool.start(db_edit_size)

    def __update_size_complete(self, pd_size: ModelProductForm):
        self.selected_size_frame.size = pd_size.size
        self.selected_size_frame.price = pd_size.price_for_sale
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm(test=False, user_data={'username': 'qwe', 'password': 'qwe'})
    w.show()
    sys.exit(app.exec())
