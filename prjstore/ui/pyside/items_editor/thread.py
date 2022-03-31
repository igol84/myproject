from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.handlers.items_editor_handler import ItemsEditorHandler


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ItemsEditorHandler)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = ItemsEditorHandler(db)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(handler)
