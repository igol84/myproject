class AbstractItem:
    pr_id: str
    pr_name: str
    pr_price: float
    pr_price_format: str

    def get_price(self) -> float:
        ...

    def hide_elements(self) -> None:
        ...
