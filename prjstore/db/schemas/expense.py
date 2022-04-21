import datetime

from pydantic import BaseModel


class BaseExpense(BaseModel):
    place_id: int
    desc: str
    date_cost: datetime.date
    cost: float


class CreateExpense(BaseExpense):
    pass


class UpdateExpense(CreateExpense):
    id: int


class Expense(BaseExpense):
    id: int

    class Config:
        orm_mode = True


class ListExpenses(BaseModel):
    __root__: list[Expense]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __str__(self):
        return str(self.__root__)

    def __len__(self):
        return len(self.__root__)
