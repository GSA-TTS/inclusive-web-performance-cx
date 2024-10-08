import pytest
from api_client.format_results import format_results


def test_format_results_normal():
    results = {
        "record": {
            "key": {"formFactor": "PHONE", "url": "https://www.wikipedia.org/"},
            "metrics": {
                "first_contentful_paint": {
                    "histogram": [
                        {"start": 0, "end": 1800, "density": 0.8874},
                        {"start": 1800, "end": 3000, "density": 0.0729},
                        {"start": 3000, "density": 0.0397},
                    ],
                    "percentiles": {"p75": 1126},
                },
                "first_input_delay": {
                    "histogram": [
                        {"start": 0, "end": 100, "density": 0.9797},
                        {"start": 100, "end": 300, "density": 0.0153},
                        {"start": 300, "density": 0.005},
                    ],
                    "percentiles": {"p75": 12},
                },
                "interaction_to_next_paint": {
                    "histogram": [
                        {"start": 0, "end": 200, "density": 0.9255},
                        {"start": 200, "end": 500, "density": 0.058},
                        {"start": 500, "density": 0.0164},
                    ],
                    "percentiles": {"p75": 104},
                },
                "largest_contentful_paint": {
                    "histogram": [
                        {"start": 0, "end": 2500, "density": 0.927},
                        {"start": 2500, "end": 4000, "density": 0.046},
                        {"start": 4000, "density": 0.027},
                    ],
                    "percentiles": {"p75": 1276},
                },
                "navigation_types": {
                    "fractions": {
                        "navigate_cache": 0.3864,
                        "reload": 0.0376,
                        "restore": 0,
                        "back_forward": 0.0522,
                        "back_forward_cache": 0.189,
                        "prerender": 0.0887,
                        "navigate": 0.2461,
                    }
                },
                "round_trip_time": {"percentiles": {"p75": 144}},
                "cumulative_layout_shift": {
                    "histogram": [
                        {"start": "0.00", "end": "0.10", "density": 0.9931},
                        {"start": "0.10", "end": "0.25", "density": 0.0061},
                        {"start": "0.25", "density": 0.0008},
                    ],
                    "percentiles": {"p75": "0.00"},
                },
                "experimental_time_to_first_byte": {
                    "histogram": [
                        {"start": 0, "end": 800, "density": 0.8677},
                        {"start": 800, "end": 1800, "density": 0.0893},
                        {"start": 1800, "density": 0.043},
                    ],
                    "percentiles": {"p75": 507},
                },
            },
            "collectionPeriod": {
                "firstDate": {"year": 2024, "month": 8, "day": 11},
                "lastDate": {"year": 2024, "month": 9, "day": 7},
            },
        },
        "urlNormalizationDetails": {
            "originalUrl": "https://www.wikipedia.org",
            "normalizedUrl": "https://www.wikipedia.org/",
        },
    }
    expected_data = {
        "url": "https://www.wikipedia.org/",
        "experimental_time_to_first_byte_p75": 507,
        "experimental_time_to_first_byte_good_density": 0.8677,
        "experimental_time_to_first_byte_needs_improvement_density": 0.0893,
        "experimental_time_to_first_byte_poor_density": 0.043,
        "first_contentful_paint_p75": 1126,
        "first_contentful_paint_good_density": 0.8874,
        "first_contentful_paint_needs_improvement_density": 0.0729,
        "first_contentful_paint_poor_density": 0.0397,
        "largest_contentful_paint_p75": 1276,
        "largest_contentful_paint_good_density": 0.927,
        "largest_contentful_paint_needs_improvement_density": 0.046,
        "largest_contentful_paint_poor_density": 0.027,
        "cumulative_layout_shift_p75": "0.00",
        "cumulative_layout_shift_good_density": 0.9931,
        "cumulative_layout_shift_needs_improvement_density": 0.0061,
        "cumulative_layout_shift_poor_density": 0.0008,
        "interaction_to_next_paint_p75": 104,
        "interaction_to_next_paint_good_density": 0.9255,
        "interaction_to_next_paint_needs_improvement_density": 0.058,
        "interaction_to_next_paint_poor_density": 0.0164,
    }
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
    expected_data = {
        "cumulative_layout_shift_good_density": None,
        "cumulative_layout_shift_needs_improvement_density": None,
        "cumulative_layout_shift_p75": None,
        "cumulative_layout_shift_poor_density": None,
        "experimental_time_to_first_byte_good_density": None,
        "experimental_time_to_first_byte_needs_improvement_density": None,
        "experimental_time_to_first_byte_p75": 100,
        "experimental_time_to_first_byte_poor_density": None,
        "first_contentful_paint_good_density": None,
        "first_contentful_paint_needs_improvement_density": None,
        "first_contentful_paint_p75": None,
        "first_contentful_paint_poor_density": None,
        "interaction_to_next_paint_good_density": None,
        "interaction_to_next_paint_needs_improvement_density": None,
        "interaction_to_next_paint_p75": None,
        "interaction_to_next_paint_poor_density": None,
        "largest_contentful_paint_good_density": None,
        "largest_contentful_paint_needs_improvement_density": None,
        "largest_contentful_paint_p75": None,
        "largest_contentful_paint_poor_density": None,
        "url": "https://example.com",
    }
    assert format_results(results) == expected_data


def test_format_results_empty_input():
    with pytest.raises(KeyError):
        format_results({})


def test_format_results_wrong_input():
    with pytest.raises(TypeError):
        format_results(None)
