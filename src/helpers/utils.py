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
