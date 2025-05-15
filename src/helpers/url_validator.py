from urllib.parse import urlparse, parse_qs

from src.helpers.models import SearchData


def assert_results_url_contains_expected_filters(url: str, expected: SearchData):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # Check location in path
    path = parsed.path.replace("-", " ").lower()
    for part in expected.location.lower().split():
        assert part in path, f"Missing location part '{part}' in path: '{parsed.path}'"

    # Check basic query params
    for key in ["adults", "children"]:
        assert str(getattr(expected, key)) == query.get(key, [None])[0], f"Mismatch for '{key}'"

    # Check check-in/check-out
    for key in ["checkin", "checkout"]:
        expected_val = getattr(expected.checkin_checkout, f"standard_format_{key}")
        actual_val = query.get(key, [None])[0]
        assert expected_val == actual_val, f"Mismatch for '{key}': expected '{expected_val}', got '{actual_val}'"
