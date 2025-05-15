from typing import Union

import allure
from playwright.sync_api import Page, TimeoutError, Error, expect, Locator

TEST_PREFIX_ID = "data-testid"


def take_screenshot_on_error(page):
    screenshot_bytes = page.screenshot(full_page=True)
    allure.attach(screenshot_bytes, attachment_type=allure.attachment_type.PNG)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def handle(self, action, description: str):
        try:
            return action()
        except TimeoutError:
            take_screenshot_on_error(self.page)
            raise TimeoutError(f"Timeout: {description}")

        except (Error, Exception) as e:
            take_screenshot_on_error(self.page)
            raise RuntimeError(f"Error during: {description}\n {str(e)}")

    def goto(self, url: str, timeout: int = 10000):
        return self.handle(lambda: self.page.goto(url, timeout=timeout), f"navigate to {url}")

    def click(self, locator: str):
        return self.handle(lambda: self.page.click(locator), f"click {locator}")

    def click_using_locator(self, locator: Locator):
        return self.handle(lambda: locator.click(), f"click {locator}")

    def fill(self, locator: str, value: str):
        return self.handle(lambda: self.page.fill(locator, value), f"fill {locator} with {value}")

    def get_text(self, locator: str) -> str:
        return self.handle(lambda: self.page.text_content(locator), f"get text from {locator}")

    def get_inner_text(self, locator: str) -> str:
        return self.handle(lambda: self.page.locator(locator).inner_text(), f"get text from {locator}")

    def get_text_from_locator(self, locator: Locator) -> str:
        return self.handle(lambda: locator.text_content(), f"get text from {locator}")

    def expect(self, locator: Union[Page, Locator]) -> None:
        return self.handle(lambda: expect(locator), f"Expecting for {locator}")

    def expect_to_have_text(self, locator: Union[Page, Locator], text: str) -> None:
        return self.handle(lambda: expect(locator).to_have_text(text), f"Expecting for {locator}")

    def expect_locator_not_to_be_empty(self, locator: Locator) -> None:
        return self.handle(lambda: expect(locator).not_to_be_empty(), f"Expecting for {locator}")

    def check_locator_visibility(self, locator: Locator) -> bool:
        return self.handle(lambda: locator.is_visible(), f"locator is_visible {locator}")

    def check_if_locator_is_enabled(self, locator: Locator) -> bool:
        return self.handle(lambda: locator.is_enabled(), f"locator is_enabled {locator}")

    def get_element(self, locator: str) -> Locator:
        return self.handle(lambda: self.page.locator(locator), f"getting element {locator}")

    def count_results(self, locator: str) -> int:
        return self.handle(lambda: self.page.locator(locator).count(), f"counting elements {locator}")

    def get_attribute(self, locator: Locator, attribute: str):
        return self.handle(lambda: locator.get_attribute(attribute), f"get attribute {locator}")

    def select_option(self, locator: str, value: str) -> int:
        return self.handle(lambda: self.page.select_option(locator, value), f"selecting element {locator}")

    def get_element_by_role(self, locator, name: str) -> Locator:
        return self.handle(lambda: self.page.get_by_role(role=locator, name=name), f"getting element by role {locator}")

    def expect_element_not_to_have_empty_text(self, locator: Locator):
        return self.handle(lambda: expect(locator).not_to_have_text("", timeout=2000),
                    f"expect element not to have count {locator}")
