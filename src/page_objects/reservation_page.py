from playwright.sync_api import Page

from src.page_objects.base_page import BasePage, TEST_PREFIX_ID


class ReservationPage(BasePage):
    PHONE_EXTENSION_SELECTOR = f'select[{TEST_PREFIX_ID}="login-signup-countrycode"]'
    MOBILE_FIELD = f"[{TEST_PREFIX_ID}='login-signup-phonenumber']"
    WHEN_TO_PAY_TEXT = "Choose when to pay"
    NAME = "#LISTING_CARD-title"
    NAME_2 = f"[{TEST_PREFIX_ID}='checkout-product-details-listing-card']"
    DATE = "[data-section-id='DATE_PICKER']"
    DATE_2 = '[data-section-id="PRODUCT_DETAILS"]'
    GUESTS = "[data-section-id='GUEST_PICKER']"
    PRICE_DETAILS = f"[{TEST_PREFIX_ID}='pd-title-ACCOMMODATION']"

    def __init__(self, page: Page):
        super().__init__(page)

    def select_country_phone_number_prefix(self):
        self.select_option(self.PHONE_EXTENSION_SELECTOR, value='972IL')

    def fill_mobile_numer(self, value: str):
        self.fill(self.MOBILE_FIELD, value)

    def choose_when_to_pay_displayed(self) -> bool:
        el = self.get_element(f"text={self.WHEN_TO_PAY_TEXT}")
        return self.check_locator_visibility(el)

    def click_next(self):
        self.click("text=Next")

    def get_item_name(self):
        name_1 = self.get_element(self.NAME)
        name_2 = self.get_element(self.NAME_2)
        if self.check_locator_visibility(name_2):
            return self.get_text_from_locator(name_2)
        else:
            return self.get_text_from_locator(name_1)


    def get_dates(self) -> str:
        return self.get_text(self.DATE)

    def get_guests_count(self) -> str:
        return self.get_inner_text(self.GUESTS)

    def get_reservation_price(self):
        return self.get_text(self.PRICE_DETAILS)
