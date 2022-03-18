from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.interface_subject import SubjectInterface


class MainWindowInterface(SubjectInterface):
    handler: MainHandler

    def start_connection(self):
        ...

    def data_changed(self, this_observer) -> None:
        ...
