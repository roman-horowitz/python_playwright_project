from playwright.sync_api import Page

from src.page_objects.base_page import BasePage, TEST_PREFIX_ID


class ProductPage(BasePage):
    LOCATION_NAME = "[data-section-id='TITLE_DEFAULT']"
    BOOKING_INFO = f"[{TEST_PREFIX_ID}='book-it-default']"
    RESERVATION_DATE = "[aria-label^='Change dates; Check-in:']"
    GUESTS_COUNT = "#GuestPicker-book_it-trigger"
    PRICE = 'div[style*="--pricing-guest-display-price-alignment"]'
    RESERVE_BUTTON = f"[{TEST_PREFIX_ID}='homes-pdp-cta-btn']"
    CHECKIN_DATE = f"[{TEST_PREFIX_ID}='change-dates-checkIn']"
    CHECKOUT_DATE = f"[{TEST_PREFIX_ID}='change-dates-checkOut']"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_location_name(self) -> str:
        el = self.get_element(self.LOCATION_NAME)
        self.expect_locator_not_to_be_empty(el)
        return self.get_text_from_locator(el).strip("ShareSave")

    def booking_info_locator(self):
        return self.get_element(self.BOOKING_INFO)

    def get_reservation_dates(self) -> str:
        el = self.booking_info_locator()
        dates = el.locator(self.RESERVATION_DATE)
        return self.get_text_from_locator(dates)

    def get_checkin_date(self):
        el = self.get_element(self.CHECKIN_DATE)
        return self.get_text_from_locator(el)

    def get_checkout_date(self):
        el = self.get_element(self.CHECKOUT_DATE)
        return self.get_text_from_locator(el)

    def get_guests_count(self) -> str:
        el = self.booking_info_locator()
        guests = el.locator(self.GUESTS_COUNT)
        return self.get_text_from_locator(guests)

    def get_price(self) -> str:
        el = self.booking_info_locator()
        price = el.locator(self.PRICE).first
        self.expect_locator_not_to_be_empty(price)
        return self.get_text_from_locator(price)

    def click_reserve(self):
        el = self.get_element(self.RESERVE_BUTTON).nth(1)
        self.expect_to_have_text(el, text="Reserve")
        self.expect_locator_not_to_be_empty(el)
        self.click_using_locator(el)
