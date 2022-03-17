from prjstore.handlers.main_handler import MainHandler


class MainWindowInterface:
    handler: MainHandler

    def start_connection(self):
        ...

    def on_update_receiving_items(self) -> None:
        ...

    def on_update_product_price_editor(self) -> None:
        ...

    def on_update_sale_registration(self) -> None:
        ...
