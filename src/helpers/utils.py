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


# TODO I don't like to do those things but I need good locators
def split_date_range_at_year(text: str) -> str:
    current_year = datetime.now().year
    for year in [current_year, current_year + 1]:
        year_str = str(year)
        if year_str in text:
            return text.split(year_str, 1)[0].strip().rstrip(",")
    raise ValueError("No valid year found in string.")


def format_date_reservation_page(text: str) -> FormattedDateRange:
    # TODO this can be done better if a dedicated element was created
    # Clean the string
    if "edit" in text.lower():
        cleaned = text.replace("Dates", "").replace("Edit", "").strip()
    else:
        cleaned = split_date_range_at_year(text)
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


# TODO I don't like to do those things but I need good locators
def extract_guest_count(text: str) -> str:
    current_year = datetime.now().year
    for year in [current_year, current_year + 1]:
        year_str = str(year)
        if year_str in text:
            guest_part = text.split(year_str, 1)[1].strip()
            break
    else:
        raise ValueError("No valid year found to isolate guest info.")

    adults = 0
    children = 0

    if "adults" in guest_part:
        parts = guest_part.split("adults")[0].strip().split()
        adults = int(parts[-1])

    if "child" in guest_part:
        parts = guest_part.split("child")[0].strip().split()
        children = int(parts[-1])
    print({"adults": adults, "children": children, "total": adults + children})
    return str(adults + children)


def format_reservation_price(reservation_page: ReservationPage):
    # TODO this can be done better if a dedicated element was created
    text = reservation_page.get_reservation_price()
    cleaned = text[1::].strip()
    price_part, nights_part = cleaned.split('x')
    return float(price_part.strip())
