import json
from deepdiff import DeepDiff
from playwright.sync_api import Page

from src.helpers.date_utils import set_date_range_data
from src.helpers.json_file_management import JsonFileManager
from src.helpers.models import SearchData, ProductData, FormattedDateRange
from src.helpers.results_scraper import extract_price
from src.helpers.utils import wait_for_results_to_load, format_date_reservation_page, format_reservation_price
from src.page_objects.general import General
from src.page_objects.main_header_filter import HomesMainHeaderFilter
from src.page_objects.product_page import ProductPage
from src.page_objects.reservation_page import ReservationPage
from src.page_objects.results_page import ResultsHeaderFilter


def open_filter_and_set_guests(header_filter, data: SearchData):
    header_filter.open_guests_filters()

    for _ in range(data.adults):
        header_filter.increase_adults()

    for _ in range(data.children):
        header_filter.increase_children()


def filter_location_main_header(header_filter: HomesMainHeaderFilter, data: SearchData) -> None:
    header_filter.set_location(data.location)
    header_filter.wait_for_first_location_result()
    header_filter.click_first_location_result()


def filter_dates_main_header(header_filter: HomesMainHeaderFilter, data: SearchData) -> None:
    if not header_filter.is_calendar_open():
        header_filter.open_checking_calendar()
    header_filter.set_checkin_date(data.checkin_checkout.standard_format_checkin)
    header_filter.set_checkout_date_date(data.checkin_checkout.standard_format_checkout)


def perform_search_with_filters(page: Page, data: SearchData) -> None:
    mhf = HomesMainHeaderFilter(page)
    General(page).go_to_url("/homes")
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
    actual = res_filter_page.get_results_date().lower()
    cico = data.checkin_checkout
    parts = [cico.checkin_day, cico.checkin_month, cico.checkout_day, cico.checkout_month]
    parts_lowered = [part.lower() for part in parts]
    for part in parts_lowered:
        assert part in actual, f"Expected '{part}' in '{actual}'"


def validate_ui_filter_results(page, data) -> None:
    rfp = ResultsHeaderFilter(page)
    validate_location_in_results_filters(rfp, data)
    validate_guests_count_in_results_filters(rfp, data)
    validate_dates_in_results_filters(rfp, data)


def format_checkin_checkout_dates_product(product_page: ProductPage) -> FormattedDateRange:
    checkin = product_page.get_checkin_date()
    checkout = product_page.get_checkout_date()
    return set_date_range_data(checkin, checkout, year_first_format=False)


def access_products_and_store_info(page, results: list[str]) -> list[ProductData]:
    pp = ProductPage(page)
    g = General(page)
    enriched_results: list[ProductData] = []
    for url in results:
        g.go_to_url(url)
        name = pp.get_location_name().lower()
        reservation_dates = format_checkin_checkout_dates_product(pp)
        guests_count = pp.get_guests_count().split()[0]
        price_text = pp.get_price()
        numeric_price = extract_price(price_text)
        total_price = int(numeric_price * reservation_dates.nights)
        # Create structured product result
        enriched_results.append(ProductData(
            name=name,
            url=url,
            checkin_checkout=reservation_dates,
            guests=guests_count,
            price_per_night=numeric_price,
            total_price=total_price
        ))

    return enriched_results


def find_cheapest_product(products: list[ProductData]) -> ProductData:
    return min(products, key=lambda x: x.price_per_night)


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
    name = reservation.get_item_name().lower().split("rating")[0]
    reservation_dates = reservation.get_dates()
    dates = format_date_reservation_page(reservation_dates)
    guests_count = reservation.get_guests_count().split("Guests")[1].split()[0]
    price = format_reservation_price(reservation)
    total_price = int(price * dates.nights)
    product = ProductData(
        name=name,
        url=page.url,
        checkin_checkout=dates,
        guests=guests_count,
        price_per_night=price,
        total_price=total_price
    )
    print(product)
    return product


def get_previous_results_and_compare(results: ProductData, json_results_file_manager: JsonFileManager):
    expected = json_results_file_manager.load()
    actual = results.model_dump()
    diff = DeepDiff(expected, actual, ignore_order=True)
    assert expected == actual, f"Snapshot mismatch:\n{json.dumps(diff, indent=2)}"
    json_results_file_manager.save(actual)
