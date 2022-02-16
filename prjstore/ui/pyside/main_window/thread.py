from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(API_DB)

    def __init__(self):
        super().__init__()
        with open('C:\\Users\\Public\\data', 'r') as file:
            lst = [line.strip() for line in file]
        self.user_data = {'username': lst[0], 'password': lst[1]}
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            db = API_DB(self.user_data)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(db)
