import sys

from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QDialogButtonBox, QMessageBox
from PySide6.QtCore import QDate, QThreadPool

from prjstore.db.schemas.sale import ShowSaleWithSLIs
from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler
from prjstore.ui.pyside.qt_utils import clearLayout
from prjstore.ui.pyside.sale_registration.components import FrameItemFactory
from prjstore.ui.pyside.sale_registration.components.abstract_product import AbstractSoldItem
from prjstore.ui.pyside.sale_registration.components.sale import Sale_Frame
from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.sale_registration_ui import Ui_Form
from prjstore.ui.pyside.sale_registration.schemas import ModelProduct, ProductId, Price, ViewProduct, ViewPlace, \
    ViewSeller, ViewSale
from prjstore.ui.pyside.sale_registration.thread import DbConnector, DBCreateSale, DBGetSales
from prjstore.ui.pyside.utils.load_widget import LoadWidget


class SaleForm(QWidget):
    items: list[ModelProduct]
    sli_list: dict[tuple[ProductId, Price]: ModelProduct]
    old_sales: list[ShowSaleWithSLIs]
    selected_item_widget: AbstractSoldItem
    selected_sli_widget: SLI_Frame
    handler: SaleRegistrationHandler

    def __init__(self, test=False):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.test = test
        self.resize(1200, 600)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.src_items.textChanged.connect(self.on_search_items_text_changed)
        self.ui.date_edit.setDate(QDate.currentDate())
        self.ui.date_edit.dateChanged.connect(self.change_data)
        self.ui.buttonBox.addButton(QPushButton('Сохранить'), QDialogButtonBox.AcceptRole)
        self.ui.buttonBox.accepted.connect(self.press_save)
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.test:
            db_connector = DbConnector()
            db_connector.signals.error.connect(self._connection_error)
            db_connector.signals.result.connect(self.set_data)
            self.thread_pool.start(db_connector)
        else:
            self.set_data((None, SaleRegistrationHandler(test=True)))

    def _connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def set_data(self, data: tuple[SaleRegistrationHandler, list[ShowSaleWithSLIs]]):
        self.handler, self.old_sales = data
        self.update()
        self.load_widget.hide()

    def update(self):
        self._update_paces_of_sales()
        self._update_sellers_names()
        self._update_sli()
        self._update_items_layout()

    def _update_paces_of_sales(self):
        self.ui.combo_box_place_of_sale.clear()
        self.ui.combo_box_place_of_sale.addItem('', userData=None)
        self.ui.combo_box_place_of_sale.currentIndexChanged.connect(self.change_data)
        for i, name_place_of_sale in self.handler.get_store_places_of_sale_names().items():
            self.ui.combo_box_place_of_sale.addItem(name_place_of_sale, userData=i)

    def _update_sellers_names(self):
        self.ui.combo_box_seller.clear()
        self.ui.combo_box_seller.addItem('', userData=None)
        self.ui.combo_box_seller.currentIndexChanged.connect(self.change_data)
        for i, seller_name in self.handler.get_store_sellers_names().items():
            self.ui.combo_box_seller.addItem(seller_name, userData=i)

    # SLI ----------------------- left panel ------------------------------
    def _update_sli(self):
        clearLayout(self.ui.sli_layout)
        self.selected_sli_widget = None
        self.sli_list = self.handler.get_sale_line_items()
        for sli in self.sli_list.values():
            product_pd = ViewProduct(id=sli.prod_id, type=sli.type, name=sli.get_desc(), price=sli.price,
                                     price_format=sli.price_format, qty=sli.qty)
            label = SLI_Frame(self, product_pd)
            self.ui.sli_layout.addWidget(label)

        for sale in self.old_sales:
            sli_list = self.handler.get_sale_line_items(sale.id)
            place_pd = ViewPlace(id=sale.place_id, desc=sale.place.name)
            seller_pd = ViewSeller(id=sale.seller_id, desc=sale.seller.name)
            list_sli_pd = []
            print(sale.sale_line_items)
            for sli in sli_list.values():
                sli_pd = ViewProduct(id=sli.prod_id, type=sli.type, name=sli.get_desc(), price=sli.price,
                                     price_format=sli.price_format, qty=sli.qty)
                list_sli_pd.append(sli_pd)
            sale_pd = ViewSale(id=sale.id, place=place_pd, seller=seller_pd, products=list_sli_pd)
            sale_frame = Sale_Frame(self, sale_pd)
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

    def _completed_getting_sales(self, pd_sales: list[ShowSaleWithSLIs]):
        self.old_sales = pd_sales
        self._update_sli()
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

    def on_click_scroll_items(self, event):
        if event:
            pass
        self._update_items_layout()

    def on_search_items_text_changed(self):
        self._update_items_layout()

    def put_on_sale(self):
        pr_id = self.selected_item_widget.pr_id
        sale_price = int(self.selected_item_widget.get_sale_price())
        sale_qty = float(self.selected_item_widget.get_sale_qty())
        self.handler.put_on_sale(pr_id, sale_qty, sale_price)
        self._update_items_layout()
        self._update_sli()
        self._update_total()
        self.ui.src_items.clear()

    def put_item_form_sli_to_items(self):
        sli_id = self.selected_sli_widget.sli_product_id
        sli_price = self.selected_sli_widget.sli_price
        self.handler.put_item_form_sli_to_items(sli_id, sli_price)
        self._update_sli()
        self._update_items_layout()
        self._update_total()

    def edit_sale_price_in_sli(self, sli_item_id: str, old_sale_price: float, sale_price: float):
        if old_sale_price != sale_price:
            self.handler.edit_sale_price_in_sli(sli_item_id, old_sale_price, sale_price)
            self._update_sli()
            self._update_total()

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
        self.load_widget.hide()
        QMessageBox(icon=QMessageBox.Information, text='Продажа выполнена!').exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SaleForm(test=False)
    w.show()
    sys.exit(app.exec())
