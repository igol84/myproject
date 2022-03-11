from PySide6.QtCore import Signal, QObject, QRunnable, Slot

from prjstore.db import API_DB
from prjstore.db.schemas.handler_product_price_editor import ModelProduct as ModelProductForm
from prjstore.db.schemas.handler_product_price_editor import ModelShoes as ModelShoesForm
from prjstore.db.schemas.handler_product_price_editor import ModelColor as ModelColorForm
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


class DBGetSales(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal()

    def __init__(self, handler, date_sale, place_id, seller_id):
        super().__init__()
        self.handler = handler
        self.date_sale = date_sale
        self.place_id = place_id
        self.seller_id = seller_id
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            self.handler.changed_date(date=self.date_sale, place_id=self.place_id, seller_id=self.seller_id)
        except OSError:
            self.signals.error.emit('Connection Error.')
        else:
            self.signals.result.emit()


class DBEditSize(QRunnable):
    class Signals(QObject):
        error = Signal(str)
        result = Signal(ModelProductForm)

    def __init__(self, handler: ProductPriceEditorHandler, pd_size: ModelProductForm):
        super().__init__()
        self.handler = handler
        self.pd_size = pd_size
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pd_size: ModelProductForm = self.handler.edit_product(self.pd_size)
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
            pd_shoes: ModelProductForm = self.handler.edit_shoes(self.pd_shoes)
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