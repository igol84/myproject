from typing import Optional

from prjstore.domain.place_of_sale import Report
from prjstore.ui.pyside.utils.format_price import format_price
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *

from prjstore.handlers.report_handler import ReportHandler
from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.report import thread
from prjstore.ui.pyside.report.ui_report import UI_Report
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class ReportPage(AbstractModule, QWidget):
    handler: ReportHandler
    current_range: Optional[ReportHandler.Range]
    current_place_id: int
    sign: str = '₴'

    def __init__(self, parent=None, user_data=None, dark_style=False):
        AbstractModule.__init__(self, parent)
        QWidget.__init__(self)
        self.name = 'report_form'
        self.observer_module_names = []
        self.__handler = None
        self.ui = UI_Report()
        self.ui.setup_ui(self)
        self.ui.combo_box_range.activated.connect(self.on_change_combo_box_range)
        self.ui.combo_box_place.activated.connect(self.on_change_combo_box_place)

        self.thread_pool = QThreadPool()
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        if dark_style:
            self.ui.setup_dark_style()
        if parent:
            if parent.dark_style:
                self.ui.setup_dark_style()
            handler = ReportHandler(main_handler=parent.handler)
            self.__connected_complete(handler)
        else:
            db_connector = thread.DbConnect(user_data)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.__connected_complete)
            self.thread_pool.start(db_connector)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        self.load_widget.hide()

    def __connected_complete(self, handler: ReportHandler):
        self.__handler = handler
        self.update_ui()
        self.load_widget.hide()

    def get_handler(self) -> ReportHandler:
        return self.__handler

    handler = property(get_handler)

    def update_data(self) -> None:
        if self.need_update:
            self.load_widget.show()
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self, updating_data: bool = True) -> None:
        if updating_data:
            self.handler.setup_store_expenses()
            self.handler.setup_store_ledger()
            self.setup_combo_box_range()
            self.setup_combo_box_place()

        reports = self.handler.get_report(range=self.current_range, place_id=self.current_place_id)
        self.setup_table(reports)

    def setup_combo_box_range(self):
        self.ui.combo_box_range.clear()
        for range_date in ReportHandler.Range:
            self.ui.combo_box_range.addItem(range_date.value, range_date)

    def setup_combo_box_place(self):
        self.ui.combo_box_place.clear()
        self.ui.combo_box_place.addItem('Все', None)
        places = self.handler.get_places()
        for place_id, place in places.items():
            self.ui.combo_box_place.addItem(place, place_id)

    def get_current_range(self) -> Optional[ReportHandler.Range]:
        return self.ui.combo_box_range.currentData()

    current_range = property(get_current_range)

    def get_current_place_id(self) -> Optional[int]:
        return self.ui.combo_box_place.currentData()

    current_place_id = property(get_current_place_id)

    def on_change_combo_box_range(self):
        self.update_ui(updating_data=False)

    def on_change_combo_box_place(self):
        self.update_ui(updating_data=False)

    def setup_table(self, reports: dict[tuple, Report]) -> None:
        clearLayout(self.ui.layout_report)
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setRowCount(len(reports))
        table.setHorizontalHeaderLabels(["Выручка", "Издержки", "Прибыль"])
        keys = list(reports.keys())
        if self.current_range == ReportHandler.Range.month:
            keys.sort(key=lambda k: (k[1], k[0]), reverse=True)
        elif self.current_range == ReportHandler.Range.year:
            keys.sort(reverse=True)
        for i, key in enumerate(keys):
            table.setVerticalHeaderItem(i, QTableWidgetItem(reports[key].head))
            total_text = f'{format_price(reports[key].total.amount, dot=True)}{self.sign}'
            expense_text = f'{format_price(reports[key].expense.amount, dot=True)}{self.sign}'
            profit_text = f'{format_price(reports[key].profit.amount, dot=True)}{self.sign}'
            table.setItem(i, 0, QTableWidgetItem(total_text))
            table.setItem(i, 1, QTableWidgetItem(expense_text))
            table.setItem(i, 2, QTableWidgetItem(profit_text))
        self.ui.layout_report.addWidget(table)


if __name__ == "__main__":
    import sys
    from prjstore.db.api import settings

    app = QApplication(sys.argv)
    w = ReportPage(user_data=settings.user_data, dark_style=True)
    w.show()
    sys.exit(app.exec())
