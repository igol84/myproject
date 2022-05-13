import sys

from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.sale_registration.components import FrameItemFactory
from prjstore.ui.pyside.sale_registration.components.abstract_product import AbstractSoldItem
from prjstore.ui.pyside.sale_registration.components.sale import Sale_Frame
from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.ui_sale_registration import Ui_SaleForm
from prjstore.ui.pyside.sale_registration.schemas import *
from prjstore.ui.pyside.sale_registration.thread import *
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.pages import PagesFrame
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout
from util.pages import Pages


class SaleForm(AbstractModule, QWidget):
    items: list[ModelProduct]
    data_items_pages: Pages
    sli_list: dict[tuple[ProductId, Price]: ModelProduct]
    old_sales: list[ViewSale]
    selected_item_widget: AbstractSoldItem
    selected_sli_widget: SLI_Frame
    handler: SaleRegistrationHandler

    def __init__(self, parent=None, dark_style=False, user_data=None):
        AbstractModule.__init__(self, parent)
        QWidget.__init__(self)
        self.name = 'sale_form'
        self.observer_module_names = ['price_editor_form', 'new_items_form', 'edit_items_form', 'report_form']
        self.thread_pool = QThreadPool()
        self.ui = Ui_SaleForm()
        self.ui.setupUi(self)
        self.data_items_pages = Pages(count_elements_on_page=11)
        self.ui.items_pages_frame = PagesFrame(parent=self, data_page=self.data_items_pages)
        self.ui.main_items_layout.addWidget(self.ui.items_pages_frame)
        self.data_items_pages.register_observer(self.ui.items_pages_frame)

        self.dark_style = dark_style
        if dark_style:
            self.setup_dark_style()
        self.ui.src_items.textChanged.connect(self.on_search_items_text_changed)
        self.ui.date_edit.setDate(QDate.currentDate())
        self.ui.date_edit.dateChanged.connect(self.on_change_data)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if parent:
            if parent.dark_style:
                self.setup_dark_style()
            self.connected_complete(SaleRegistrationHandler(main_handler=self.parent.handler))
        else:
            db_connector = DbConnect(user_data)
            db_connector.signals.error.connect(self._connection_error)
            db_connector.signals.result.connect(self.connected_complete)
            self.thread_pool.start(db_connector)

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
        self.update_ui()
        self.load_widget.hide()

    def update_ui(self):
        self._update_paces_of_sales()
        self._update_sellers_names()
        self._update_sli()
        self._update_items_layout()
        self.on_change_data()

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
        date_sale = self.ui.date_edit.date().toPython()
        self.old_sales = self.handler.get_old_sales(date_sale)
        for dp_sale in self.old_sales:
            sale_frame = Sale_Frame(self, dp_sale)
            self.ui.sli_layout.addWidget(sale_frame)
        self.ui.sli_layout.addStretch(0)

    def _update_total(self):
        date_sale = self.ui.date_edit.date().toPython()
        self.ui.total.setText(self.handler.get_total(date_sale))

    def on_change_data(self):
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
    def _update_items_layout(self, update_data: bool = True):
        if update_data:
            self.items = self.handler.get_store_items(search=self.ui.src_items.text())
            self.data_items_pages.count_elements = len(self.items)
        clearLayout(self.ui.items_layout)
        self.selected_item_widget = None

        for i in self.data_items_pages.items_on_page:
            item = self.items[i]
            item_frame = FrameItemFactory.create(product_type=item.type, parent=self, item_pd=item)
            self.ui.items_layout.addWidget(item_frame)
        self.ui.items_layout.addStretch(0)

    def on_search_items_text_changed(self):
        self.data_items_pages.selected_page = 1
        self._update_items_layout()

    def update_data(self):
        if self.need_update:
            self.update_ui()
            self.need_update = False

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
        if self.parent:
            self.parent.data_changed(self)
        self.ui.src_items.clear()

    def _items_page_number_changed(self):
        self._update_items_layout(update_data=False)

    # _______________________________________

    def page_number_changed(self, data_pages):
        if data_pages is self.data_items_pages:
            self._items_page_number_changed()

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
        if self.parent:
            self.parent.data_changed(self)
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
        if self.parent:
            self.parent.data_changed(self)
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
        self.update_ui()
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()


if __name__ == "__main__":
    from prjstore.db.api import settings

    app = QApplication(sys.argv)
    w = SaleForm(dark_style=True, user_data=settings.user_data)
    w.show()
    sys.exit(app.exec())
