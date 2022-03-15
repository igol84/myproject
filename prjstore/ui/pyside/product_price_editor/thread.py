from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import ModelColorForm
from prjstore.db.schemas.handler_product_price_editor import ModelShoesForm
from prjstore.db.schemas.handler_product_price_editor import ModelSizeForm
from prjstore.db.schemas.handler_product_price_editor import ModelProductForm
from prjstore.handlers.product_price_editor_handler import ProductPriceEditorHandler


class DbConnect(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ProductPriceEditorHandler)

    def __init__(self, user_data, db: API_DB = None):
        super().__init__()
        self.signals = self.Signals()
        self.db = db
        self.user_data = user_data

    @Slot()
    def run(self):
        try:
            db = self.db if self.db else API_DB(self.user_data)
            handler = ProductPriceEditorHandler(db)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit(handler)


class DBEditProduct(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ModelProductForm)

    def __init__(self, handler: ProductPriceEditorHandler, pd_data: ModelProductForm):
        super().__init__()
        self.handler = handler
        self.pd_data = pd_data
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_data: ModelSizeForm = self.handler.edit_product(self.pd_data)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_data)


class DBEditSize(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ModelSizeForm)

    def __init__(self, handler: ProductPriceEditorHandler, pd_size: ModelSizeForm):
        super().__init__()
        self.handler = handler
        self.pd_size = pd_size
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_size: ModelSizeForm = self.handler.edit_size(self.pd_size)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_size)


class DBEditShoes(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ModelShoesForm)

    def __init__(self, handler: ProductPriceEditorHandler, pd_shoes: ModelShoesForm):
        super().__init__()
        self.handler = handler
        self.pd_shoes = pd_shoes
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_shoes: ModelSizeForm = self.handler.edit_shoes(self.pd_shoes)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_shoes)


class DBEditColor(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ModelColorForm)

    def __init__(self, handler: ProductPriceEditorHandler, pd_color: ModelShoesForm):
        super().__init__()
        self.handler = handler
        self.pd_color = pd_color
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_shoes: ModelColorForm = self.handler.edit_color(self.pd_color)
        except OSError:
            self.signals.error.emit('Нет подключения к интернету.')
        else:
            self.signals.result.emit(pd_shoes)
