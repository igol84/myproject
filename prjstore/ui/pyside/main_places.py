import sys
from typing import Optional

from prjstore.handlers.places_editor_handler import PlacesEditorHandler
from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface
from prjstore.ui.pyside.places_editor import schemas
from prjstore.ui.pyside.places_editor import thread
from prjstore.ui.pyside.places_editor.components.add_place_widget import AddPlaceWidget
from prjstore.ui.pyside.places_editor.components.place_widget import PlaceWidget
from prjstore.ui.pyside.places_editor.ui_places_editor import UI_PlacesEditor
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout


class PlacesEditor(QWidget, ObserverInterface):
    __pd_places: list[schemas.ViewPlace]
    __selected_place_id: Optional[int]
    __place_widgets: dict[int, PlaceWidget]
    __handler: PlacesEditorHandler
    __dark_style: bool

    def __init__(self, parent=None, test=False, user_data=None, list_pd_places=None, db=None, dark_style=False):
        super().__init__()
        self.parent: MainWindowInterface = parent
        if parent:
            self.parent.register_observer(self)
        self.__handler = None
        self.test = test
        self.ui = UI_PlacesEditor()
        self.ui.setup_ui(self)
        self.user_data = user_data
        self.db = db
        self.thread_pool = QThreadPool()
        self.dark_style = dark_style
        if list_pd_places is None:
            list_pd_places = []
        self.list_pd_places: list = list_pd_places
        self.__selected_place_id = None
        self.__place_widgets = {}
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')

        if not self.parent:
            if not self.test:
                db_connector = thread.DbConnect(self.user_data, self.db)
                db_connector.signals.error.connect(self.__connection_error)
                db_connector.signals.result.connect(self.__connected_complete)
                self.thread_pool.start(db_connector)
            else:
                self.__connected_complete(PlacesEditorHandler(db=None, test=True))
        else:
            store = self.parent.handler.store
            self.__connected_complete(PlacesEditorHandler(db=self.db, store=store))

    def get_selected_place_id(self) -> int:
        return self.__selected_place_id

    def set_selected_place_id(self, selected_place_id: Optional[int]) -> None:
        if self.selected_place_id:
            self.selected_widget.selected = False
        if selected_place_id is not None:
            self.__selected_place_id = selected_place_id
            self.selected_widget.selected = True
        else:
            self.__selected_place_id = None

    selected_place_id = property(get_selected_place_id, set_selected_place_id)

    def get_selected_widget(self) -> PlaceWidget:
        if self.selected_place_id:
            return self.__place_widgets[self.selected_place_id]

    selected_widget = property(get_selected_widget)

    def get_dark_style(self) -> bool:
        return self.__dark_style

    def set_dark_style(self, flag: bool) -> None:
        self.__dark_style = flag
        if flag:
            self.setStyleSheet(
                '#PlacesEditor, #PlacesFrame {background-color: #2F303B; color: #F8F8F2;}\n'
                'QLabel {color: #F8F8F2;}\n'
            )

    dark_style = property(get_dark_style, set_dark_style)

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: PlacesEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self, store=None) -> None:
        self.load_widget.show()
        self.handler.update_data(store)
        self.update_ui()
        self.load_widget.hide()

    def update_ui(self) -> None:
        clearLayout(self.ui.layout_places)
        self.__pd_places = self.handler.get_store_places()
        self.ui.layout_places.addWidget(AddPlaceWidget(self))
        for pd_place in self.__pd_places:
            item_frame = PlaceWidget(pd_place, self)
            self.__place_widgets[pd_place.place_id] = item_frame
            self.ui.layout_places.addWidget(item_frame)
        if self.selected_place_id:
            self.set_selected_place_id(self.selected_place_id)

    def on_clicked_label_name(self, place_id: int) -> None:
        self.selected_place_id = place_id

    def on_edit_place_name(self, place_id: int, new_name: str):
        self.load_widget.show()
        db_place = thread.DBEditPlaceName(self.handler, place_id, new_name)
        db_place.signals.error.connect(self.__connection_error)
        db_place.signals.result.connect(self.__update_place_name_complete)
        self.thread_pool.start(db_place)

    def __update_place_name_complete(self, place_id: int, new_name: str):
        self.__place_widgets[place_id].name = new_name
        self.__place_widgets[place_id].selected = False
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def on_changed_active(self, place_id: int, active: bool):
        self.load_widget.show()
        db_place = thread.DBEditPlaceActive(self.handler, place_id, active)
        db_place.signals.error.connect(self.__connection_error)
        db_place.signals.compleate.connect(self.__update_place_active_complete)
        self.thread_pool.start(db_place)

    def __update_place_active_complete(self):
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def on_add_place(self, name: str):
        self.load_widget.show()
        db_place = thread.DBAddPlace(self.handler, name)
        db_place.signals.error.connect(self.__connection_error)
        db_place.signals.result.connect(self.__adding_place_complete)
        self.thread_pool.start(db_place)

    def __adding_place_complete(self, pd_new_place: schemas.ViewPlace):
        item_frame = PlaceWidget(pd_new_place, self)
        self.__place_widgets[pd_new_place.place_id] = item_frame
        self.ui.layout_places.insertWidget(1, item_frame)
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PlacesEditor(test=False, user_data={'username': 'qwe', 'password': 'qwe'}, dark_style=True)
    w.show()
    sys.exit(app.exec())
