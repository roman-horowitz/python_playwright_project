from src.helpers.utils import wait_for_results_to_load, check_if_pagination_available
from src.page_objects.results_page import Items, ResultsPagination


def extract_price(price_text: str) -> int:
    parts = price_text.split()
    if "originally" in parts:
        raw_price = parts[1][1:]  # skip currency symbol
    else:
        raw_price = parts[0][1:]
    numeric_price = int(raw_price.replace(",", ""))
    return numeric_price


def is_card_inside_content_scroller(card) -> bool:
    return card.evaluate("node => !!node.closest('[data-testid=\"content-scroller\"]')")


def scrape_visible_5_star_cards(page, seen_links, base_url):
    cards = Items(page)
    wait_for_results_to_load(page)
    counted_cards = cards.count_results_items()
    for i in range(counted_cards):
        card = cards.get_items().nth(i)
        if is_card_inside_content_scroller(card):
            continue
        cards.expect_for_price()
        if not cards.top_rating_visible(card):
            continue
        link = cards.get_item_link(card)
        if link and link not in seen_links:
            seen_links.add(f"{base_url}{link}")


def scroll_and_scrape_all_top_rated_results(page, base_url) -> list[str]:
    seen_links = set()
    while True:
        scrape_visible_5_star_cards(page, seen_links, base_url)
        if not check_if_pagination_available(page):
            break
        else:
            ResultsPagination(page).pagination_click_next()
    return list(seen_links)
