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


def format_date_reservation_page(reservation_page: ReservationPage) -> str:
    cleaned = reservation_page.get_dates().lower()
    cleaned = cleaned.replace("–", "")
    cleaned = cleaned.replace("dates", "")
    cleaned = cleaned.replace("edit", "")
    parts = cleaned.split("\u2009")
    return "".join(parts)


def format_reservation_price(reservation_page: ReservationPage):
    text = reservation_page.get_reservation_price()
    cleaned = text[1::].strip()
    price_part, nights_part = cleaned.split('x')
    price = float(price_part.strip())
    nights = int(nights_part.strip().split()[0])
    return price, nights
