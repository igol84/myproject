import math

from prjstore.ui.pyside.interface_subject import SubjectInterface


class Pages(SubjectInterface):
    __count_elements: int
    __count_elements_on_page: int
    __selected_page: int

    __count_pages: int = None
    __items_on_page: list

    __default_cont_elements_on_page: int = 15

    def __init__(self, count_elements: int = 0, count_elements_on_page: int = None, selected_page: int = 1):
        self.__count_elements = count_elements
        if count_elements_on_page:
            self.__count_elements_on_page = count_elements_on_page
        else:
            self.__count_elements_on_page = self.__default_cont_elements_on_page
        self.__selected_page = selected_page
        self.observers = []
        self.update_pages_data()

    def register_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        del self.observers[observer]

    def notify_observer(self, this_observer=None) -> None:
        for observer in self.observers:
            observer.update_pages(self.count_pages, self.selected_page)

    def __get_count_elements(self) -> int:
        return self.__count_elements

    def __set_count_elements(self, count_elements: int) -> None:
        self.__count_elements = count_elements
        self.update_pages_data()

    count_elements = property(__get_count_elements, __set_count_elements)

    def __get_count_elements_on_page(self) -> int:
        return self.__count_elements_on_page

    def __set_count_elements_on_page(self, count_elements_on_page: int) -> None:
        self.__count_elements_on_page = count_elements_on_page
        self.update_pages_data()

    count_elements_on_page = property(__get_count_elements_on_page, __set_count_elements_on_page)

    def __get_selected_page(self) -> int:
        return self.__selected_page

    def __set_selected_page(self, selected_page: int) -> None:
        if selected_page <= self.count_pages:
            self.__selected_page = selected_page
            self.update_pages_data()

    selected_page = property(__get_selected_page, __set_selected_page)

    def __get_count_pages(self) -> int:
        return self.__count_pages

    count_pages = property(__get_count_pages)

    def __get_items_on_page(self) -> set:
        return self.__items_on_page

    items_on_page = property(__get_items_on_page)

    def update_pages_data(self):
        self.__count_pages = math.ceil(self.count_elements / self.count_elements_on_page)
        firs_element = self.count_elements_on_page * (self.selected_page - 1)
        qty_of_show = self.count_elements_on_page
        if self.count_elements < self.count_elements_on_page:
            qty_of_show = self.count_elements
        if self.count_elements - firs_element < self.count_elements_on_page:
            qty_of_show = self.count_elements - firs_element
        self.__items_on_page = [i for i in range(firs_element, firs_element + qty_of_show)]
        self.notify_observer()

    def __repr__(self):
        return f'count_elements: {self.count_elements}\n' \
               f'count_elements_on_page: {self.count_elements_on_page}\n' \
               f'selected_page: {self.selected_page}\n' \
               f'{"=" * 40}\n' \
               f'count_pages: {self.count_pages}\n' \
               f'items_on_page: {self.items_on_page}'


if __name__ == '__main__':
    pages = Pages(count_elements=400, count_elements_on_page=15)
    pages.selected_page = 1
    print(pages.items_on_page)
    pages.selected_page = 2
    print(pages.items_on_page)
    pages.selected_page = 3
    print(pages.items_on_page)
