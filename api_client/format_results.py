"""
Formats results from CrUX API Response
"""


def format_results(results):
    """Format results for csv file"""
    metrics = results["record"]["metrics"]

    data = [
        results["record"]["key"]["url"],
        metrics.get("experimental_time_to_first_byte", {})
        .get("percentiles", {})
        .get("p75", None),
        metrics.get("first_contentful_paint", {})
        .get("percentiles", {})
        .get("p75", None),
        metrics.get("largest_contentful_paint", {})
        .get("percentiles", {})
        .get("p75", None),
        metrics.get("cumulative_layout_shift", {})
        .get("percentiles", {})
        .get("p75", None),
        metrics.get("interaction_to_next_paint", {})
        .get("percentiles", {})
        .get("p75", None),
    ]

    return data


if __name__ == "__main__":
    pass
