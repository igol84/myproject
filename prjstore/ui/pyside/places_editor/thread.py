from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.db.schemas import place as schemas
from prjstore.handlers.places_editor_handler import PlacesEditorHandler
from prjstore.ui.pyside.places_editor import schemas as view_schemas


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(PlacesEditorHandler)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = PlacesEditorHandler(db)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(handler)


class DBEditPlaceName(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(int, str)

    def __init__(self, handler: PlacesEditorHandler, place_id: int, new_name: str):
        super().__init__()
        self.handler = handler
        self.place_id = place_id
        self.new_name = new_name
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_data: schemas.Place = self.handler.edit_name(self.place_id, self.new_name)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_data.id, pd_data.name)


class DBEditPlaceActive(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        compleate = Signal()

    def __init__(self, handler: PlacesEditorHandler, place_id: int, active: bool):
        super().__init__()
        self.handler = handler
        self.place_id = place_id
        self.active = active
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.edit_active(self.place_id, self.active)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.compleate.emit()


class DBAddPlace(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: PlacesEditorHandler, name: str):
        super().__init__()
        self.handler = handler
        self.name = name
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.add_place(self.name)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()
