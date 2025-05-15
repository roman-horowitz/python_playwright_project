import random
from datetime import datetime, timedelta

from src.helpers.models import FormattedDateRange


def get_random_date_range(
        start_days_from_today=3,
        max_days_from_today=30,
        min_stay_nights=2,
        max_stay_nights=14
) -> tuple[str, str]:
    today = datetime.today()
    checkin_offset = random.randint(start_days_from_today, max_days_from_today)
    stay_length = random.randint(min_stay_nights, max_stay_nights)

    checkin = today + timedelta(days=checkin_offset)
    checkout = checkin + timedelta(days=stay_length)

    return checkin.strftime("%Y-%m-%d"), checkout.strftime("%Y-%m-%d")


def set_date_range_data(checkin, checkout, year_first_format: bool = True) -> FormattedDateRange:
    formatting = "%Y-%m-%d" if year_first_format else "%m/%d/%Y"
    checkin_date = datetime.strptime(checkin, formatting).date()
    checkout_date = datetime.strptime(checkout, formatting).date()

    ci_month = checkin_date.strftime("%b")
    ci_day = str(int(checkin_date.strftime("%d")))
    co_month = checkout_date.strftime("%b")
    co_day = str(int(checkout_date.strftime("%d")))

    total_days = (checkout_date - checkin_date).days

    return FormattedDateRange(
        checkin_month=ci_month,
        checkin_day=ci_day,
        checkout_month=co_month,
        checkout_day=co_day,
        nights=total_days
    )
