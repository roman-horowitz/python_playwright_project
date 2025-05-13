import random
from datetime import datetime, timedelta


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


def format_date_range_for_ui(checkin, checkout):
    checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
    checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

    ci_month, ci_day = checkin.strftime("%b"), str(int(checkin.strftime("%d")))
    co_month, co_day = checkout.strftime("%b"), str(int(checkout.strftime("%d")))
    return ci_month, ci_day, co_month, co_day
