from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB, schemas
from prjstore.handlers.receiving_the_items_handler import ReceivingTheItemsHandler


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ReceivingTheItemsHandler)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = ReceivingTheItemsHandler(db)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(handler)


class DBSaveData(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: ReceivingTheItemsHandler, data: schemas.header_receiving_the_items.ModelProduct):
        super().__init__()
        self.handler = handler
        self.data = data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.save_data(data=self.data)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()
