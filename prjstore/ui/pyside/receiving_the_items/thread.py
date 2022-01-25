from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.receiving_the_items_handler import ReceivingTheItemsHandler


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ReceivingTheItemsHandler)

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            db = API_DB()
            handler = ReceivingTheItemsHandler(db=db)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(handler)


class DBGetProducts(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal()

    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.get_products()
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit()

