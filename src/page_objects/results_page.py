from playwright.sync_api import Page, Locator

from src.page_objects.base_page import BasePage, TEST_PREFIX_ID


class ResultsHeaderFilter(BasePage):
    SEARCH_RESULTS_LOCATION_NAME = f"[{TEST_PREFIX_ID}='little-search-location']"
    SEARCH_RESULTS_DATES = f"[{TEST_PREFIX_ID}='little-search-date']"
    SEARCH_RESULTS_GUESTS = f"[{TEST_PREFIX_ID}='little-search-guests']"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_results_location_name(self) -> str:
        return self.get_text(self.SEARCH_RESULTS_LOCATION_NAME)

    def get_results_date(self) -> str:
        return self.get_text(self.SEARCH_RESULTS_DATES)

    def get_guest_count(self) -> str:
        return self.get_text(self.SEARCH_RESULTS_GUESTS)


class Items(BasePage):
    GALLERY = f"[{TEST_PREFIX_ID}='content-scroller']"
    RESULTS_CARDS = f"[{TEST_PREFIX_ID}='card-container']"
    RATING = "text=5.0 out of 5 average rating"
    PRICE_MAIN = f"[{TEST_PREFIX_ID}='price-availability-row']"
    PRICE_SUB = ":text('per night')"

    def __init__(self, page: Page):
        super().__init__(page)

    def count_results_items(self) -> int:
        return self.count_results(self.RESULTS_CARDS)

    def expect_for_price(self):
        self.expect(self.get_element(self.PRICE_MAIN))

    def top_rating_visible(self, item: Locator) -> bool:
        return self.check_locator_visibility(item.locator(self.RATING))

    def get_items(self) -> Locator:
        return self.get_element(self.RESULTS_CARDS)

    def get_price(self, item: Locator)-> str:
        return self.get_text_from_locator(item.locator(self.PRICE_SUB))

    def get_item_link(self, item: Locator) -> str:
        return self.get_attribute(item.locator("a").first, "href")

class ResultsPagination(BasePage):
    PAGINATION = "[aria-label='Search results pagination']"
    NEXT_BUTTON = '[aria-label="Next"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def pagination_is_visible(self):
        pagination = self.get_element(self.PAGINATION)
        return self.check_locator_visibility(pagination)

    def pagination_next_button(self) -> Locator:
        pagination = self.get_element(self.PAGINATION).locator(self.NEXT_BUTTON)
        return pagination.first

    def pagination_next_button_is_enabled(self) -> bool:
        pagination = self.pagination_next_button()
        return self.check_if_locator_is_enabled(pagination)

    def pagination_next_button_is_visible(self) -> bool:
        pagination = self.pagination_next_button()
        return self.check_locator_visibility(pagination)

    def pagination_click_next(self) -> None:
        pagination = self.pagination_next_button()
        return self.click_using_locator(pagination)
