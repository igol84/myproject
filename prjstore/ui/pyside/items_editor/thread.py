from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.db.schemas import handler_items_editor as schemas
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


class DBEditItem(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(schemas.ItemFormEdit)

    def __init__(self, handler: ItemsEditorHandler, pd_data: schemas.ItemFormEdit):
        super().__init__()
        self.handler = handler
        self.pd_data = pd_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_data: schemas.ItemFormEdit = self.handler.edit_item(self.pd_data)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_data)


class DBDeleteItem(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        complete = Signal()

    def __init__(self, handler: ItemsEditorHandler, item_id: int):
        super().__init__()
        self.handler = handler
        self.item_id = item_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.delete_item(self.item_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.complete.emit()


class DBGetSales(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(list)

    def __init__(self, handler: ItemsEditorHandler, item_id: int):
        super().__init__()
        self.handler = handler
        self.item_id = item_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_sales: list[schemas.SaleDetail] = self.handler.get_item_sales(self.item_id)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_sales)
