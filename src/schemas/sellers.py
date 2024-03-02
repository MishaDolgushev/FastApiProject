from pydantic import BaseModel
from pydantic import EmailStr, StringConstraints
from typing_extensions import Annotated

__all__ = ["BaseSeller", "ReturnedSeller", "IncomingSeller", "ReturnedAllSellers"]

from src.schemas.books import ReturnedBook


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ReturnedSeller(BaseSeller):
    id: int
    books: list[ReturnedBook]
    pass


class IncomingSeller(BaseSeller):
    first_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    email: EmailStr
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=100)]


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
