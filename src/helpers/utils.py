from datetime import datetime
from src.helpers.models import FormattedDateRange
from src.page_objects.reservation_page import ReservationPage
from src.page_objects.results_page import ResultsPagination


def wait_for_results_to_load(page):
    if check_if_pagination_available:
        wait_for_cards_to_load(page, expected_min=18)
    else:
        wait_for_cards_to_load(page, expected_min=1)


def check_if_pagination_available(page):
    pr = ResultsPagination(page)
    if not pr.pagination_is_visible():
        print("No pagination found — likely no results.")
        return False
    if pr.pagination_next_button_is_visible() and pr.pagination_next_button_is_enabled():
        return True
    else:
        return False


def wait_for_cards_to_load(page, timeout=10000, expected_min=1):
    page.wait_for_function(
        f"""
        () => {{
            const cards = [...document.querySelectorAll('[data-testid="card-container"]')];
            const visible = cards.filter(c => !c.closest('[data-testid="content-scroller"]'));
            return visible.length >= {expected_min};
        }}
        """,
        timeout=timeout
    )


def format_date_reservation_page(text: str) -> FormattedDateRange:
    # TODO this can be done better if a dedicated element was created
    # Clean the string
    cleaned = text.replace("Dates", "").replace("Edit", "").strip()

    # Split on the en-dash separator (surrounded by narrow spaces)
    parts = cleaned.split("\u2009–\u2009")

    checkin_part = parts[0].strip()  # e.g., "Jun 2"
    checkout_part = parts[1].strip()  # e.g., "8" or "Jul 5"

    # Parse check-in
    ci_month, ci_day = checkin_part.split()

    # Parse checkout
    co_parts = checkout_part.split()
    if len(co_parts) == 1:
        co_month = ci_month  # same month
        co_day = co_parts[0]
    else:
        co_month, co_day = co_parts

    year = datetime.now().year
    checkin_date = datetime.strptime(f"{ci_month} {ci_day} {year}", "%b %d %Y").date()
    checkout_date = datetime.strptime(f"{co_month} {co_day} {year}", "%b %d %Y").date()
    nights = (checkout_date - checkin_date).days

    return FormattedDateRange(
        checkin_month=ci_month,
        checkin_day=ci_day,
        checkout_month=co_month,
        checkout_day=co_day,
        nights=nights,
        standard_format_checkin=str(checkin_date),
        standard_format_checkout=str(checkout_date)
    )


def format_reservation_price(reservation_page: ReservationPage):
    # TODO this can be done better if a dedicated element was created
    text = reservation_page.get_reservation_price()
    cleaned = text[1::].strip()
    price_part, nights_part = cleaned.split('x')
    return float(price_part.strip())
