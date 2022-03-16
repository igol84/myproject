import sys

from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.utils.qt_utils import clearLayout
from prjstore.ui.pyside.sale_registration.components import FrameItemFactory
from prjstore.ui.pyside.sale_registration.components.abstract_product import AbstractSoldItem
from prjstore.ui.pyside.sale_registration.components.sale import Sale_Frame
from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.sale_registration_ui import Ui_Form
from prjstore.ui.pyside.sale_registration.schemas import *
from prjstore.ui.pyside.sale_registration.thread import *
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *


class SaleForm(QWidget):
    items: list[ModelProduct]
    sli_list: dict[tuple[ProductId, Price]: ModelProduct]
    old_sales: list[ShowSaleWithSLIs]
    selected_item_widget: AbstractSoldItem
    selected_sli_widget: SLI_Frame
    handler: SaleRegistrationHandler

    def __init__(self, parent=None, dark_style=False, test=False, user_data=None, db=None):
        super().__init__()
        self.parent: MainWindowInterface = parent
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.test = test
        self.resize(1200, 600)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.dark_style = dark_style
        if dark_style:
            self.setup_dark_style()
        self.ui.src_items.textChanged.connect(self.on_search_items_text_changed)
        self.ui.date_edit.setDate(QDate.currentDate())
        self.ui.date_edit.dateChanged.connect(self.change_data)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.test:
            db_connector = DbConnect(self.user_data, self.db)
            db_connector.signals.error.connect(self._connection_error)
            db_connector.signals.result.connect(self.connected_complete)
            self.thread_pool.start(db_connector)
        else:
            self.connected_complete(SaleRegistrationHandler(test=True))

    def setup_dark_style(self):
        self.setStyleSheet(
            '#SaleForm, #title {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            'QLineEdit {background-color: #121212; color: #dcdcdc;}\n'
            '#widget_slis, #widget_items {background-color: #2F303B; border:2px solid #484B5E;  color: #F8F8F2;}'
        )

    def _connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def connected_complete(self, handler: SaleRegistrationHandler):
        self.handler = handler
        self.update()
        self.load_widget.hide()

    def update(self):
        self._update_paces_of_sales()
        self._update_sellers_names()
        self._update_sli()
        self._update_items_layout()
        self.change_data()

    def _update_paces_of_sales(self):
        self.ui.combo_box_place_of_sale.clear()
        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        for i, name_place_of_sale in self.handler.get_store_places_of_sale_names().items():
            self.ui.combo_box_place_of_sale.addItem(name_place_of_sale, userData=i)

    def _update_sellers_names(self):
        self.ui.combo_box_seller.clear()
        self.ui.combo_box_seller.addItem('', userData=None)
        for i, seller_name in self.handler.get_store_sellers_names().items():
            self.ui.combo_box_seller.addItem(seller_name, userData=i)

    # SLI ----------------------- left panel ------------------------------
    def _update_sli(self):
        clearLayout(self.ui.sli_layout)
        self.selected_sli_widget = None
        self.sli_list = self.handler.get_sale_line_items()
        for sli in self.sli_list.values():
            product_pd = ViewProduct(prod_id=sli.prod_id, type=sli.type, name=sli.get_desc(), price=sli.price,
                                     price_format=sli.price_format, qty=sli.qty)
            label = SLI_Frame(self, product_pd)
            self.ui.sli_layout.addWidget(label)
        if self.sli_list:
            btn_new_sale = QPushButton('Сохранить')
            self.ui.sli_layout.addWidget(btn_new_sale, alignment=Qt.AlignRight)
            btn_new_sale.clicked.connect(self.press_save)
        # Old sales
        self.old_sales = self.handler.get_old_sales()
        for dp_sale in self.old_sales:
            sale_frame = Sale_Frame(self, dp_sale)
            self.ui.sli_layout.addWidget(sale_frame)
        self.ui.sli_layout.addStretch(0)

    def _update_total(self):
        self.ui.total.setText(self.handler.get_total())

    def change_data(self):
        date_sale = self.ui.date_edit.date().toPython()
        place_id = self.ui.combo_box_place_of_sale.currentData()
        seller_id = self.ui.combo_box_seller.currentData()
        self.load_widget.show()
        db_get_sales = DBGetSales(self.handler, date_sale, place_id, seller_id)
        db_get_sales.signals.error.connect(self._connection_error)
        db_get_sales.signals.result.connect(self._completed_getting_sales)
        self.thread_pool.start(db_get_sales)

    def _completed_getting_sales(self):
        self._update_sli()
        self._update_total()
        self.load_widget.hide()

    # Items -------------------- right panel --------------------------------
    def _update_items_layout(self):
        clearLayout(self.ui.items_layout)
        self.selected_item_widget = None
        self.items = self.handler.get_store_items(search=self.ui.src_items.text())
        for item in self.items:
            item_frame = FrameItemFactory.create(product_type=item.type, parent=self, item_pd=item)
            self.ui.items_layout.addWidget(item_frame)
        self.ui.items_layout.addStretch(0)

    def on_search_items_text_changed(self):
        self._update_items_layout()

    def update_items_data(self):
        self.load_widget.show()
        self.handler.update_data()
        self._update_items_layout()
        self.load_widget.hide()

    def put_on_sale(self):
        pr_id = self.selected_item_widget.pr_id
        sale_price = int(self.selected_item_widget.get_sale_price())
        sale_qty = float(self.selected_item_widget.get_sale_qty())
        thread = DBPutOnSale(self.handler, pr_id, sale_qty, sale_price)
        thread.signals.error.connect(self._connection_error)
        thread.signals.complete.connect(self._completed_put_on_sale)
        self.thread_pool.start(thread)

    def _completed_put_on_sale(self):
        self._update_items_layout()
        self._update_sli()
        self._update_total()
        self.ui.src_items.clear()

    def put_item_form_sli_to_items(self, sale_id=None):
        pr_id = self.selected_sli_widget.sli_product_id
        sli_price = self.selected_sli_widget.sli_price
        if sale_id:
            self.load_widget.show()
            thread = DbPutItemFormSliToItems(self.handler, pr_id=pr_id, sli_price=sli_price, sale_id=sale_id)
            thread.signals.error.connect(self._connection_error)
            thread.signals.complete.connect(self._completed_put_item_form_sli_to_items)
            self.thread_pool.start(thread)
        else:
            self.handler.put_item_form_sli_to_items(pr_id=pr_id, sli_price=sli_price)
            self._completed_put_item_form_sli_to_items()

    def _completed_put_item_form_sli_to_items(self):
        self._update_sli()
        self._update_items_layout()
        self._update_total()
        self.load_widget.hide()

    def edit_sale_price_in_sli(self, sli_prod_id: str, old_sale_price: float, new_sale_price: float, sale_id=None):
        if old_sale_price != new_sale_price:
            if not sale_id:
                self.handler.edit_sale_price_in_sli(sli_prod_id, old_sale_price, new_sale_price)
                self._completed_edit_price()
            else:
                self.load_widget.show()
                thread = DbEditSalePrice(self.handler, sale_id, sli_prod_id, old_sale_price, new_sale_price)
                thread.signals.error.connect(self._connection_error)
                thread.signals.complete.connect(self._completed_edit_price)
                self.thread_pool.start(thread)

    def _completed_edit_price(self):
        self._update_sli()
        self._update_total()
        self.load_widget.hide()

    def press_save(self):
        warning_texts = []
        if not self.ui.combo_box_place_of_sale.currentText():
            warning_texts.append('Не вабрано место продажи!')
        if not self.ui.combo_box_seller.currentText():
            warning_texts.append('Не вабран продавец!')
        if not self.sli_list:
            warning_texts.append('Нет товаров в списке продаж!')
        if warning_texts:
            QMessageBox(icon=QMessageBox.Warning, text='\n'.join(warning_texts)).exec()
        else:
            current_data = self.ui.date_edit.date().toPython()
            current_place_id = self.ui.combo_box_place_of_sale.currentData()
            current_seller_id = self.ui.combo_box_seller.currentData()
            self.load_widget.show()
            db_create_sale = DBCreateSale(self.handler, current_data, current_place_id, current_seller_id)
            db_create_sale.signals.error.connect(self._connection_error)
            db_create_sale.signals.complete.connect(self._completed_sale)
            self.thread_pool.start(db_create_sale)

    def _completed_sale(self):
        self.update()
        if self.parent:
            self.parent.on_update_sale_registration()
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm(test=False, dark_style=True, user_data={'username': 'qwe', 'password': 'qwe'})
    w.show()
    sys.exit(app.exec())
