import logging

from playwright.sync_api import Page

from src.helpers.actions_booking_flow import perform_search_with_filters, validate_ui_filter_results, \
    access_products_and_store_info, find_cheapest_product, fill_phone_number, go_to_top_cheapest_and_validate_result, \
    get_previous_results_and_compare
from src.helpers.results_scraper import scroll_and_scrape_all_top_rated_results
from src.helpers.url_validator import assert_results_url_contains_expected_filters


def test_reserve_cheapest_top_rated_apartment(page: Page, search_data, base_url, json_results_file_manager):
    perform_search_with_filters(page, search_data)
    assert_results_url_contains_expected_filters(page.url, search_data)
    validate_ui_filter_results(page, search_data)
    top_results = scroll_and_scrape_all_top_rated_results(page, base_url)
    product_info_results = access_products_and_store_info(page, top_results)
    cheapest = find_cheapest_product(product_info_results)
    logging.info(cheapest)
    json_results_file_manager.save(cheapest.model_dump())
    result = go_to_top_cheapest_and_validate_result(page, cheapest.url)
    get_previous_results_and_compare(result, json_results_file_manager)
    fill_phone_number(page, "501234567")
