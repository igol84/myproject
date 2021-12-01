from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB


class DbConnectorSignals(QObject):
    error = Signal(str)
    result = Signal(API_DB)


class DbConnector(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = DbConnectorSignals()

    @Slot()
    def run(self):
        try:
            db = API_DB()
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(db)


class CreateSaleSignals(QObject):
    error = Signal(str)
    complete = Signal()


class DBCreateSale(QRunnable):
    def __init__(self, handler, current_data, current_place_of_sale_id, current_seller_id):
        super().__init__()
        self.handler = handler
        self.current_data = current_data
        self.current_place_of_sale_id = current_place_of_sale_id
        self.current_seller_id = current_seller_id
        self.signals = CreateSaleSignals()

    @Slot()
    def run(self):
        try:
            self.handler.end_sale(self.current_data, self.current_place_of_sale_id, self.current_seller_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()
