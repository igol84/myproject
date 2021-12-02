from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.sale_registration_handler import SaleRegistrationHandler


class DbConnectorSignals(QObject):
    error = Signal(str)
    result = Signal(tuple)


class DbConnector(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = DbConnectorSignals()

    @Slot()
    def run(self):
        try:
            db = API_DB()
            handler = SaleRegistrationHandler(db=db)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit((db, handler))


class CreateSaleSignals(QObject):
    error = Signal(str)
    complete = Signal()


class DBCreateSale(QRunnable):
    def __init__(self, db,  handler, current_data, current_place_of_sale_id, current_seller_id):
        super().__init__()
        self.db = db
        self.handler = handler
        self.current_data = current_data
        self.current_place_of_sale_id = current_place_of_sale_id
        self.current_seller_id = current_seller_id
        self.signals = CreateSaleSignals()

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
