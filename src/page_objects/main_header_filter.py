from playwright.sync_api import Page

from src.page_objects.base_page import BasePage, TEST_PREFIX_ID


class MainHeaderFilter(BasePage):
    LOCATION_FILTER = "#bigsearch-query-location-input"
    FIRST_LOCATION = f"[{TEST_PREFIX_ID}='option-0']"
    GUESTS_BUTTON = f"[{TEST_PREFIX_ID}='structured-search-input-field-guests-button']"
    INCREASE_ADULTS = f"[{TEST_PREFIX_ID}='stepper-adults-increase-button']"
    INCREASE_CHILDREN = f"[{TEST_PREFIX_ID}='stepper-children-increase-button']"
    SEARCH_BUTTON = f"[{TEST_PREFIX_ID}='structured-search-input-search-button']"
    DATES_SECTION = "text=Add dates"
    CALENDAR = '[aria-label="Calendar"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def set_location(self, city: str):
        self.fill(self.LOCATION_FILTER, city)

    def wait_for_location_field_to_be_available(self):
        el = self.get_element(self.LOCATION_FILTER)
        self.expect(el)

    def increase_adults(self):
        self.click(self.INCREASE_ADULTS)

    def increase_children(self):
        self.click(self.INCREASE_CHILDREN)

    def search(self):
        self.click(self.SEARCH_BUTTON)

    def is_dates_section_open(self) -> bool:
        el = self.get_element(self.CALENDAR).first
        return self.check_locator_visibility(el)

    def open_dates_section(self):
        self.click(self.DATES_SECTION)

    def set_checkin_date(self, checkin_date: str):
        el = self.get_element(f"[data-state--date-string='{checkin_date}']")
        self.click_using_locator(el.first)

    def set_checkout_date_date(self, checkout_date: str):
        el = self.get_element(f"[data-state--date-string='{checkout_date}']")
        self.click_using_locator(el.first)

    def wait_for_first_location_result(self):
        self.expect(self.get_element(self.FIRST_LOCATION))

    def click_first_location_result(self):
        self.click(self.FIRST_LOCATION)

    def open_guests_filters(self):
        self.click(self.GUESTS_BUTTON)
