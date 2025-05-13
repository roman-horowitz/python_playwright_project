from playwright.sync_api import Page

from src.page_objects.base_page import BasePage, TEST_PREFIX_ID


class MainHeaderFilter(BasePage):
    LOCATION_FILTER = "#bigsearch-query-location-input"
    FIRST_LOCATION = f"[{TEST_PREFIX_ID}='option-0']"
    GUESTS_BUTTON = f"[{TEST_PREFIX_ID}='structured-search-input-field-guests-button']"
    INCREASE_ADULTS = f"[{TEST_PREFIX_ID}='stepper-adults-increase-button']"
    INCREASE_CHILDREN = f"[{TEST_PREFIX_ID}='stepper-children-increase-button']"
    SEARCH_BUTTON = f"[{TEST_PREFIX_ID}='structured-search-input-search-button']"

    def __init__(self, page: Page):
        super().__init__(page)

    def set_location(self, city: str):
        self.fill(self.LOCATION_FILTER, city)

    def increase_adults(self):
        self.click(self.INCREASE_ADULTS)

    def increase_children(self):
        self.click(self.INCREASE_CHILDREN)

    def search(self):
        self.click(self.SEARCH_BUTTON)

    def set_checkin_date(self, checkin_date: str):
        self.click(f"[data-state--date-string='{checkin_date}']")

    def set_checkout_date_date(self, checkout_date: str):
        self.click(f"[data-state--date-string='{checkout_date}']")

    def wait_for_first_location_result(self):
        self.expect(self.get_element(self.FIRST_LOCATION))

    def click_first_location_result(self):
        self.click(self.FIRST_LOCATION)

    def open_guests_filters(self):
        self.click(self.GUESTS_BUTTON)
