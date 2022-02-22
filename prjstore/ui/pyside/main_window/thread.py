from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(API_DB)

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            db = API_DB(self.user_data)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(db)
