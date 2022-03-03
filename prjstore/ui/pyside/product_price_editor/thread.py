from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.product_price_editor_handler import ProductPriceEditor


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ProductPriceEditor)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = ProductPriceEditor(db)
        except OSError:
            self.signals.error.emit('Connection Error.')
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
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit()
