import pytest
from api_client.format_results import format_results


def test_format_results_normal():
    results = {
        "record": {
            "key": {"url": "https://example.com"},
            "metrics": {
                "experimental_time_to_first_byte": {"percentiles": {"p75": 100}},
                "first_contentful_paint": {"percentiles": {"p75": 200}},
                "largest_contentful_paint": {"percentiles": {"p75": 300}},
                "cumulative_layout_shift": {"percentiles": {"p75": 400}},
                "interaction_to_next_paint": {"percentiles": {"p75": 500}},
            },
        }
    }
    expected_data = ["https://example.com", 100, 200, 300, 400, 500]
    assert format_results(results) == expected_data


def test_format_results_missing_metrics():
    results = {
        "record": {
            "key": {"url": "https://example.com"},
            "metrics": {
                "experimental_time_to_first_byte": {"percentiles": {"p75": 100}},
            },
        }
    }
    expected_data = ["https://example.com", 100, None, None, None, None]
    assert format_results(results) == expected_data


def test_format_results_no_data():
    results = {
        "record": {
            "key": {"url": "https://example.com"},
            "metrics": {},
        }
    }
    expected_data = ["https://example.com", None, None, None, None, None]
    assert format_results(results) == expected_data


def test_format_results_empty_input():
    with pytest.raises(KeyError):
        format_results({})


def test_format_results_wrong_input():
    with pytest.raises(TypeError):
        format_results(None)
