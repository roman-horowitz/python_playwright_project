from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class General(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_url(self, url: str):
        self.goto(url)
