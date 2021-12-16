from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(SaleRegistrationHandler)

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            db = API_DB()
            handler = SaleRegistrationHandler(db=db)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(handler)


class DBGetSales(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal()

    def __init__(self, handler, date_sale, place_id, seller_id):
        super().__init__()
        self.handler = handler
        self.date_sale = date_sale
        self.place_id = place_id
        self.seller_id = seller_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.changed_date(date=self.date_sale, place_id=self.place_id, seller_id=self.seller_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit()


class DBCreateSale(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler, current_data, current_place_of_sale_id, current_seller_id):
        super().__init__()
        self.handler = handler
        self.current_data = current_data
        self.current_place_of_sale_id = current_place_of_sale_id
        self.current_seller_id = current_seller_id
        self.signals = self.Signals()

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


class DBPutOnSale(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: SaleRegistrationHandler, pr_id: str, sale_qty: int, sale_price: float):
        super().__init__()
        self.handler = handler
        self.pr_id = pr_id
        self.sale_qty = sale_qty
        self.sale_price = sale_price
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.put_on_sale(pr_id=self.pr_id, qty=self.sale_qty, sale_price=self.sale_price)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()


class DbPutItemFormSliToItems(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: SaleRegistrationHandler, pr_id: str, sli_price: float, sale_id: int = None):
        super().__init__()
        self.handler = handler
        self.pr_id = pr_id
        self.sli_price = sli_price
        self.sale_id = sale_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.put_item_form_sli_to_items(pr_id=self.pr_id, sli_price=self.sli_price, sale_id=self.sale_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()
