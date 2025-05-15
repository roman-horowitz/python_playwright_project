from typing import Optional

from pydantic import BaseModel


class FormattedDateRange(BaseModel):
    checkin_month: str
    checkin_day: str
    checkout_month: str
    checkout_day: str
    nights: Optional[int]
    standard_format_checkin: Optional[str]
    standard_format_checkout: Optional[str]


class SearchData(BaseModel):
    location: str
    adults: int
    children: int
    checkin_checkout: FormattedDateRange


class ProductData(BaseModel):
    name: str
    url: str
    checkin_checkout: FormattedDateRange
    guests: str
    price_per_night: float
    total_price: int
