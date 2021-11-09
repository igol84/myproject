class AbstractSoldItem:
    pr_id: str
    pr_name: str
    pr_price: float
    pr_price_format: str
    pr_qty: int

    def get_sale_price(self) -> float:
        ...

    def get_sale_qty(self) -> int:
        ...
