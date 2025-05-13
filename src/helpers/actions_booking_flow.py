import difflib
import json
import logging

from playwright.sync_api import Page

from src.helpers.date_utils import format_date_range_for_ui
from src.helpers.json_file_management import JsonFileManager
from src.helpers.models import SearchData, ProductData
from src.helpers.results_scraper import extract_price
from src.helpers.utils import wait_for_results_to_load
from src.page_objects.general import General
from src.page_objects.main_header_filter import MainHeaderFilter
from src.page_objects.product_page import ProductPage
from src.page_objects.reservation_page import ReservationPage
from src.page_objects.results_page import ResultsHeaderFilter


def open_filter_and_set_guests(header_filter, data: SearchData):
    header_filter.open_guests_filters()

    for _ in range(data.adults):
        header_filter.increase_adults()

    for _ in range(data.children):
        header_filter.increase_children()


def filter_location_main_header(header_filter: MainHeaderFilter, data: SearchData) -> None:
    header_filter.set_location(data.location)
    header_filter.wait_for_first_location_result()
    header_filter.click_first_location_result()


def filter_dates_main_header(header_filter: MainHeaderFilter, data: SearchData) -> None:
    # TODO add validate the window is open
    header_filter.set_checkin_date(data.checkin)
    header_filter.set_checkout_date_date(data.checkout)


def perform_search_with_filters(page: Page, data: SearchData) -> None:
    mhf = MainHeaderFilter(page)
    filter_location_main_header(mhf, data)
    filter_dates_main_header(mhf, data)
    open_filter_and_set_guests(mhf, data)
    mhf.search()
    wait_for_results_to_load(page)


def validate_location_in_results_filters(res_filter_page: ResultsHeaderFilter, data: SearchData) -> None:
    location_name_result = res_filter_page.get_results_location_name()
    lower_city = data.location.lower()
    for i in lower_city.split():
        assert i in location_name_result.lower(), f"expected {i} in location results but was missing"


def validate_guests_count_in_results_filters(res_filter_page: ResultsHeaderFilter, data: SearchData) -> None:
    search_results_guests_filter = res_filter_page.get_guest_count()
    lower_result = search_results_guests_filter.lower()
    actual_count = lower_result.strip('guests').strip()
    assert str(data.adults + data.children) == actual_count


def validate_dates_in_results_filters(res_filter_page: ResultsHeaderFilter, data: SearchData) -> None:
    actual = res_filter_page.get_results_date()
    ci_month, ci_day, co_month, co_day = format_date_range_for_ui(data.checkin, data.checkout)
    parts = [ci_month, ci_day, co_day] if ci_month == co_month else [ci_month, co_month, ci_day, co_day]
    for part in parts:
        assert part in actual, f"Expected '{part}' in '{actual}'"


def validate_ui_filter_results(page, data) -> None:
    rfp = ResultsHeaderFilter(page)
    validate_location_in_results_filters(rfp, data)
    validate_guests_count_in_results_filters(rfp, data)
    validate_dates_in_results_filters(rfp, data)


def access_products_and_store_info(page, results: list[str]) -> list[ProductData]:
    pp = ProductPage(page)
    g = General(page)
    enriched_results: list[ProductData] = []

    for url in results:
        g.go_to_url(url)
        page.goto(url)
        name = pp.get_location_name()
        reservation_dates = pp.get_reservation_dates()
        guests_count = pp.get_guests_count().split()[0]
        price_text = pp.get_price()
        numeric_price = extract_price(price_text)
        # Create structured product result
        enriched_results.append(ProductData(
            name=name,
            url=url,
            checkin_checkout=reservation_dates,
            guests=guests_count,
            price=numeric_price
        ))

    return enriched_results


def find_cheapest_product(products: list[ProductData]) -> ProductData:
    return min(products, key=lambda x: x.price)


def fill_phone_number(page, phone: str):
    reservation = ReservationPage(page)
    if reservation.choose_when_to_pay_displayed():
        reservation.click_next()
    reservation.select_country_phone_number_prefix()
    reservation.fill_mobile_numer(phone)


def go_to_top_cheapest_and_validate_result(page, cheapest: str):
    General(page).go_to_url(cheapest)
    ProductPage(page).click_reserve()
    reservation = ReservationPage(page)
    name = reservation.get_item_name()
    dates = reservation.get_dates()
    guests_count = reservation.get_guests_count().split("Guests")[1].split()[0]
    raw_price = reservation.get_average_price().split()[1][1::]
    price = round(float(raw_price.replace(",", "")))
    product = ProductData(
        name=name,
        url=page.url,
        checkin_checkout=dates,
        guests=guests_count,
        price=price
    )
    logging.info(product)
    return product


def get_previous_results_and_compare(results: ProductData, json_results_file_manager: JsonFileManager):
    expected = json_results_file_manager.load()
    actual = results.model_dump()
    expected_json = json.dumps(expected, indent=2, sort_keys=True)
    actual_json = json.dumps(actual, indent=2, sort_keys=True)

    diff = difflib.unified_diff(
        expected_json.splitlines(),
        actual_json.splitlines(),
        fromfile="expected",
        tofile="actual",
        lineterm=""
    )
    diff_output = "\n".join(diff)
    if diff_output:
        print("Mismatch detected:\n")
        print(diff_output)
    else:
        print("Objects match.")
    json_results_file_manager.save(actual)

