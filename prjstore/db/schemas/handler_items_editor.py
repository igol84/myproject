import datetime

from pydantic import BaseModel

from prjstore.ui.pyside.utils.format_price import format_price


class ItemFormEdit(BaseModel):
    id: int
    new_qty: int
    new_price: float


class SaleDetail(BaseModel):
    sale_id: int
    date: datetime.date
    qty: int
    price: float

    def get_text(self, sign: str) -> str:
        date = self.date.strftime("%d-%m-%Y")
        return f'{self.sale_id}:  {date} - {self.qty}шт - {format_price(self.price, dot=True)}{sign}'


class ListSaleDetail(BaseModel):
    __root__: list[SaleDetail]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)
