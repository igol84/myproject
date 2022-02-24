from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.db.api.authorizations import AuthException


class DbConnect(QRunnable):
    class Signals(QObject):
        connection_error = Signal(str)
        authentication_error = Signal(str)
        result = Signal(API_DB)

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            db = API_DB(self.user_data)
        except ConnectionError:
            self.signals.connection_error.emit('Connection Error.')
        except AuthException:
            self.signals.authentication_error.emit('Authentication Error.')
        else:
            self.signals.result.emit(db)
