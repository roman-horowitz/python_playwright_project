from urllib.parse import urlparse, parse_qs

from src.helpers.models import SearchData


def assert_results_url_contains_expected_filters(url: str, expected_filters: SearchData):
    convert_to_dict  = expected_filters.model_dump()
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    for key, expected_value in convert_to_dict.items():
        if key == "location":
            location_parts = expected_value.lower().split()
            path = parsed.path.replace("-", " ").lower()
            for part in location_parts:
                assert part in path, f"Missing location part '{part}' in URL path: '{parsed.path}'"
        else:
            actual_value = query_params.get(key)[0]
            assert actual_value is not None, f"Missing filter '{key}' in URL query"
            assert str(
                expected_value) in actual_value, f"Filter mismatch for '{key}': expected '{expected_value}', got '{actual_value}'"
