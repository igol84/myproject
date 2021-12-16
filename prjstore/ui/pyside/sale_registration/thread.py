import datetime

from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler


class DbConnector(QRunnable):
    class DbConnectorSignals(QObject):
        error = Signal(str)
        result = Signal(SaleRegistrationHandler)

    def __init__(self):
        super().__init__()
        self.signals = self.DbConnectorSignals()

    @Slot()
    def run(self):
        try:
            db = API_DB()
            handler = SaleRegistrationHandler(db=db)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(handler)


class DBCreateSale(QRunnable):
    class CreateSaleSignals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler, current_data, current_place_of_sale_id, current_seller_id):
        super().__init__()
        self.handler = handler
        self.current_data = current_data
        self.current_place_of_sale_id = current_place_of_sale_id
        self.current_seller_id = current_seller_id
        self.signals = self.CreateSaleSignals()

    @Slot()
    def run(self):
        try:
            self.handler.end_sale(self.current_data, self.current_place_of_sale_id, self.current_seller_id)
            if self.handler.is_complete():
                self.handler.new_sale()
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()


class DBGetSales(QRunnable):
    class GetSalesSignals(QObject):
        error = Signal(str)
        result = Signal()

    def __init__(self, handler, date_sale, place_id, seller_id):
        super().__init__()
        self.handler = handler
        self.date_sale = date_sale
        self.place_id = place_id
        self.seller_id = seller_id
        self.signals = self.GetSalesSignals()

    @Slot()
    def run(self):
        try:
            self.handler.changed_date(date=self.date_sale, place_id=self.place_id, seller_id=self.seller_id)
            # sorted_pd_sales = sorted(pd_sales, key=lambda sale: (sale.place.id, sale.seller.id, sale.date_time))
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit()
