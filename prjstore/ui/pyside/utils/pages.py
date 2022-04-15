from prjstore.ui.pyside.utils.qt_core import *


class ParentInterface:
    def page_number_changed(self) -> None:
        ...


class PagesFrame(QFrame):
    __count_pages: int
    __selected_page: int

    def __init__(self, parent=None, count_pages: int = 1, selected_page: int = 1, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent: ParentInterface = parent
        self.__count_pages = count_pages
        self.__selected_page = selected_page

        self.btn_first = Btn('<<')
        self.btn_previous = Btn('<')
        self.line_edit = LineEdit(parent=self)
        self.btn_next = Btn('>')
        self.btn_last = Btn('>>')

        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.btn_first)
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.btn_next)
        self.layout.addWidget(self.btn_last)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.btn_first.clicked.connect(self.on_clicked_first)
        self.btn_previous.clicked.connect(self.on_clicked_previous)
        self.btn_next.clicked.connect(self.on_clicked_next)
        self.btn_last.clicked.connect(self.on_clicked_last)

        self.__update()

    def __get_selected_page(self) -> int:
        return self.__selected_page

    def __set_selected_page(self, selected_page: int) -> None:
        self.__selected_page = selected_page
        self.__update()

    selected_page = property(__get_selected_page, __set_selected_page)

    def __get_count_pages(self) -> int:
        return self.__count_pages

    def __set_count_pages(self, count_pages: int) -> None:
        self.__count_pages = count_pages
        self.__update()

    count_pages = property(__get_count_pages, __set_count_pages)

    def __update(self):
        self.btn_first.setEnabled(True)
        self.btn_previous.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.btn_last.setEnabled(True)
        if self.selected_page == 1:
            self.btn_first.setEnabled(False)
            self.btn_previous.setEnabled(False)
        if self.selected_page == self.count_pages:
            self.btn_next.setEnabled(False)
            self.btn_last.setEnabled(False)
        self.line_edit.update_text()

    def on_clicked_first(self):
        if self.parent:
            self.parent.selected_page = 1
        else:
            self.selected_page = 1

    def on_clicked_previous(self):
        if self.parent:
            self.parent.selected_page = self.selected_page - 1
        else:
            self.selected_page -= 1

    def on_clicked_next(self):
        if self.parent:
            self.parent.selected_page = self.selected_page + 1
        else:
            self.selected_page += 1

    def on_clicked_last(self):
        if self.parent:
            self.parent.selected_page = self.count_pages
        else:
            self.selected_page = self.count_pages

    def update_pages(self, count_pages, selected_page):
        self.__count_pages = count_pages
        if self.parent and self.__selected_page != selected_page:
            self.parent.page_number_changed()
            self.__selected_page = selected_page
        self.__update()


class Btn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(24)


class LineEdit(QLineEdit):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent: PagesFrame = parent
        self.setFixedWidth(100)

    def update_text(self) -> None:
        text = f'{self.parent.selected_page} из {self.parent.count_pages}'
        self.setText(text)
        self.clearFocus()

    def focusInEvent(self, arg__1: QFocusEvent) -> None:
        text = f'{self.parent.selected_page}'
        self.setText(text)
        QLineEdit.focusInEvent(self, arg__1)

    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        self.update_text()
        QLineEdit.focusOutEvent(self, arg__1)


if __name__ == '__main__':
    import sys

    from PySide6 import QtWidgets
    from PySide6.QtWidgets import QComboBox

    app = QtWidgets.QApplication(sys.argv)
    window = QWidget()
    h_box = QtWidgets.QHBoxLayout()
    btn = PagesFrame(count_pages=20, selected_page=1)

    h_box.addWidget(btn)
    window.setLayout(h_box)

    window.show()
    sys.exit(app.exec())
