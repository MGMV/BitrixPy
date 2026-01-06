
from typing import TypedDict


class ContactItem(TypedDict):
    #: str
    Имя: str
    Email: list[str]

class DealItem(TypedDict):
    #: str
    Название: str
    Сумма: str
    Контакты: list[ContactItem]

class Response(TypedDict):
    status: str
    deals: list[DealItem]