import sys

from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.product_price_editor import schemas
from prjstore.ui.pyside.product_price_editor.components import FrameProductFactory, ShoesFrame, ProductFrame
from prjstore.ui.pyside.product_price_editor.components.abstract_product import AbstractItem
from prjstore.ui.pyside.product_price_editor.components.shoes_comps import SizeFrame, ColorFrame
from prjstore.ui.pyside.product_price_editor.thread import *
from prjstore.ui.pyside.product_price_editor.ui_product_price_edit import UI_Frame
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class PriceEditor(QWidget):
    products: list[schemas.ModelProduct]
    selected_item_widget: AbstractItem
    handler: ProductPriceEditorHandler

    def __init__(self, parent=None, test=False, user_data=None, list_pd_product=None, db=None, dark_style=False):
        super().__init__()
        self.parent: MainWindowInterface = parent
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.test = test
        self.dark_style = dark_style
        if list_pd_product is None:
            list_pd_product = []
        self.list_pd_prod: list = list_pd_product
        self.resize(500, 600)
        self.ui = UI_Frame()
        self.ui.setup_ui(self)
        if self.dark_style:
            self.setup_dark_style()
        self.selected_product_frame: ProductFrame = None
        self.selected_shoes_frame: ShoesFrame = None
        self.selected_color_frame: ColorFrame = None
        self.selected_size_frame: SizeFrame = None
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        self.ui.src_products.textChanged.connect(self.on_search_text_changed)

        if not self.test:
            db_connector = DbConnect(self.user_data, self.db)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.connected_complete)
            self.thread_pool.start(db_connector)

    def setup_dark_style(self):
        self.setStyleSheet(
            '#ProductPriceEdit, #ProductFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            'QLineEdit {background-color: #121212; color: #dcdcdc;}\n'
            '#widget_slis, #widget_items {background-color: #2F303B; border:2px solid #484B5E;  color: #F8F8F2;}'
        )

    def on_search_text_changed(self):
        self.load_widget.show()
        self.update_items_layout()
        self.load_widget.hide()

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def connected_complete(self, handler: ProductPriceEditorHandler):
        self.handler = handler
        self.update_items_layout()
        self.load_widget.hide()

    def update_data(self):
        self.load_widget.show()
        self.handler.update_data()
        self.update_items_layout()
        self.load_widget.hide()

    def update_items_layout(self):
        self.products = self.handler.get_store_products(search=self.ui.src_products.text())
        clearLayout(self.ui.layout)
        self.selected_item_widget = None
        for item in self.products:
            item_frame = FrameProductFactory.create(product_type=item.type, parent=self, item_pd=item)
            self.ui.layout.addWidget(item_frame)

    def on_press_edit_simple_product(self, product_frame: ProductFrame):
        self.selected_product_frame = product_frame
        pr_id = product_frame.pr_id
        new_name = product_frame.line_edit_name.text()
        new_price = product_frame.line_edit_price.text()
        pd_data = ModelProductForm(id=pr_id, new_name=new_name, new_price=new_price)
        self.load_widget.show()
        db_edit_product = DBEditProduct(self.handler, pd_data)
        db_edit_product.signals.error.connect(self.__connection_error)
        db_edit_product.signals.result.connect(self.__update_product_complete)
        self.thread_pool.start(db_edit_product)

    def __update_product_complete(self, pd_data: ModelProductForm):
        self.selected_product_frame.name = pd_data.new_name
        self.selected_product_frame.price = pd_data.new_price
        if self.parent:
            self.parent.on_update_product_price_editor()
        self.load_widget.hide()

    def on_press_edit_by_name(self, shoes_frame: ShoesFrame):
        self.selected_shoes_frame = shoes_frame
        name = shoes_frame.name
        new_price = shoes_frame.desc_frame.price_line_edit.text()
        new_price = new_price if new_price else None
        new_name = shoes_frame.desc_frame.line_edit_desc.text()
        ps_shoes = ModelShoesForm(name=name, new_name=new_name, price_for_sale=new_price)
        self.load_widget.show()
        db_edit_shoes = DBEditShoes(self.handler, ps_shoes)
        db_edit_shoes.signals.error.connect(self.__connection_error)
        db_edit_shoes.signals.result.connect(self.__update_shoes_complete)
        self.thread_pool.start(db_edit_shoes)

    def __update_shoes_complete(self, pd_shoes: ModelShoesForm):
        self.selected_shoes_frame.desc_frame.selected = False
        if pd_shoes.price_for_sale is not None:
            self.selected_shoes_frame.set_price_of_all_sizes(pd_shoes.price_for_sale)
        if pd_shoes.new_name is not None:
            self.selected_shoes_frame.name = pd_shoes.new_name
        if self.selected_shoes_frame.selected_size_frame:
            self.selected_shoes_frame.selected_size_frame.selected = False
        if self.parent:
            self.parent.on_update_product_price_editor()
        self.load_widget.hide()

    def on_press_edit_by_color(self, pr_name: str, color_frame: ColorFrame):
        self.selected_color_frame = color_frame
        color = color_frame.color
        new_color = color_frame.header.line_edit_color.text()
        price = color_frame.header.line_edit_price.text()
        price = price if price else None
        ps_color = ModelColorForm(name=pr_name, color=color, new_color=new_color, price_for_sale=price)
        self.load_widget.show()
        db_edit_color = DBEditColor(self.handler, ps_color)
        db_edit_color.signals.error.connect(self.__connection_error)
        db_edit_color.signals.result.connect(self.__update_color_complete)
        self.thread_pool.start(db_edit_color)

    def __update_color_complete(self, pd_color: ModelColorForm):
        self.selected_color_frame.color = pd_color.new_color
        if pd_color.price_for_sale is not None:
            self.selected_color_frame.set_price_of_all_sizes(pd_color.price_for_sale)
        if self.parent:
            self.parent.on_update_product_price_editor()
        self.load_widget.hide()

    def on_edit_size(self, size_frame: SizeFrame):
        self.selected_size_frame = size_frame
        pr_id = size_frame.pr_id
        size = size_frame.line_edit_size.text()
        price = size_frame.line_edit_price.text()
        pd_size = ModelSizeForm(id=pr_id, size=size, price_for_sale=price)
        self.load_widget.show()
        db_edit_size = DBEditSize(self.handler, pd_size)
        db_edit_size.signals.error.connect(self.__connection_error)
        db_edit_size.signals.result.connect(self.__update_size_complete)
        self.thread_pool.start(db_edit_size)

    def __update_size_complete(self, pd_size: ModelSizeForm):
        self.selected_size_frame.size = pd_size.size
        self.selected_size_frame.price = pd_size.price_for_sale
        self.load_widget.hide()
        if self.parent:
            self.parent.on_update_product_price_editor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PriceEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
