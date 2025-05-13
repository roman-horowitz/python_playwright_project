from pydantic import BaseModel


class SearchData(BaseModel):
    location: str
    adults: int
    children: int
    checkin: str
    checkout: str


class ProductData(BaseModel):
    name: str
    url: str
    checkin_checkout: str
    guests: str
    price: int
