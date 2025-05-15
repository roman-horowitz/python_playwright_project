import pytest
from playwright.sync_api import Page

from src.helpers.date_utils import get_random_date_range, set_date_range_data
from src.helpers.json_file_management import JsonFileManager
from src.helpers.models import SearchData


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("base_url")


@pytest.fixture(autouse=True)
def open_base_url_and_store_storage_values(page: Page) -> None:
    page.goto("/")
    key = "__amplify__translation_engine/TRANSLATION_ANNOUNCEMENT"
    value = {"data": {"pdp": 1747053960240}, "expires": None}
    page.evaluate("""({ key, value }) => {localStorage.setItem(key, JSON.stringify(value));}""",
                  arg={"key": key, "value": value})


@pytest.fixture
def search_data_from_json() -> dict:
    manager = JsonFileManager("data/test_find_top_cheapest_data.json")
    return manager.load()


@pytest.fixture
def json_results_file_manager() -> JsonFileManager:
    manager = JsonFileManager("../temp/top_cheapest_place.json")
    return manager


@pytest.fixture
def search_data(search_data_from_json) -> SearchData:
    checkin, checkout = get_random_date_range()
    checkin_checkout = set_date_range_data(checkin, checkout)
    checkin_checkout.standard_format_checkin = checkin
    checkin_checkout.standard_format_checkout = checkout

    return SearchData(
        location=search_data_from_json.get("location", "Tel Aviv"),
        adults=search_data_from_json.get("adults", 2),
        children=search_data_from_json.get("children", 2),
        checkin_checkout=checkin_checkout,
    )
