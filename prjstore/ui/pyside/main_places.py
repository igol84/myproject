import sys
from typing import Optional

from prjstore.handlers.places_editor_handler import PlacesEditorHandler
from prjstore.ui.pyside.abstract_module import AbstractModule
from prjstore.ui.pyside.places_editor import schemas
from prjstore.ui.pyside.places_editor import thread
from prjstore.ui.pyside.places_editor.components.add_place_widget import AddPlaceWidget
from prjstore.ui.pyside.places_editor.components.place_widget import PlaceWidget
from prjstore.ui.pyside.places_editor.ui_places_editor import UI_PlacesEditor
from prjstore.ui.pyside.utils.load_widget import LoadWidget
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.qt_utils import clearLayout
from util.pages import Pages


class PlacesEditor(AbstractModule, QWidget, Pages):
    __handler: PlacesEditorHandler
    __pd_places: list[schemas.ViewPlace]
    __selected_place_id: Optional[int]
    __place_widgets: dict[int, PlaceWidget]

    def __init__(self, parent=None, user_data=None, dark_style=False):
        AbstractModule.__init__(self, parent)
        QWidget.__init__(self)
        self.name = 'places_form'
        self.observer_module_names = ['sale_form']
        self.__handler = None
        self.ui = UI_PlacesEditor()
        self.ui.setup_ui(self)

        Pages.__init__(self, count_elements_on_page=13)
        self.register_observer(self.ui.pages_frame)

        self.thread_pool = QThreadPool()

        self.__selected_place_id = None
        self.__place_widgets = {}
        self.load_widget = LoadWidget(parent=self, path='utils/loading.gif')
        if dark_style:
            self.setup_dark_style()
        if parent:
            self.parent.register_observer(self)
            if parent.dark_style:
                self.setup_dark_style()
            self.__connected_complete(PlacesEditorHandler(main_handler=parent.handler))
        else:
            db_connector = thread.DbConnect(user_data)
            db_connector.signals.error.connect(self.__connection_error)
            db_connector.signals.result.connect(self.__connected_complete)
            self.thread_pool.start(db_connector)

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

    def setup_dark_style(self) -> None:
        self.setStyleSheet(
            '#PlacesEditor, #PlacesFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            'QLabel {color: #F8F8F2;}\n'
        )

    def __connection_error(self, err: str):
        QMessageBox.warning(self, err, err)
        sys.exit(app.exec())

    def __connected_complete(self, handler: PlacesEditorHandler):
        self.handler = handler
        self.update_ui()
        self.load_widget.hide()

    def update_data(self) -> None:
        if self.need_update:
            self.load_widget.show()
            self.update_ui()
            self.need_update = False
            self.load_widget.hide()

    def update_ui(self, updating_data: bool = True) -> None:
        clearLayout(self.ui.layout_places)
        if updating_data:
            self.__pd_places = self.handler.get_store_places()
            self.count_elements = len(self.__pd_places)
        self.ui.layout_places.addWidget(AddPlaceWidget(self))
        for i in self.items_on_page:
            item_frame = PlaceWidget(self.__pd_places[i], self)
            self.__place_widgets[self.__pd_places[i].place_id] = item_frame
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
        db_place.signals.complete.connect(self.__adding_place_complete)
        self.thread_pool.start(db_place)

    def __adding_place_complete(self):
        self.update_ui()
        self.selected_page = 1
        if self.parent:
            self.parent.data_changed(self)
        self.load_widget.hide()

    def page_number_changed(self, data_page):
        if data_page:
            self.update_ui(updating_data=False)


if __name__ == "__main__":
    from prjstore.db.api import settings

    app = QApplication(sys.argv)
    w = PlacesEditor(user_data=settings.user_data, dark_style=True)
    w.show()
    sys.exit(app.exec())
