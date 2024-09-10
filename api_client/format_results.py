"""
Formats results from CrUX API Response
"""


def format_results(results):
    """Format results for csv file"""
    metrics = results["record"]["metrics"]

    ttfb = metrics.get("experimental_time_to_first_byte", {})
    fcp = metrics.get("first_contentful_paint", {})
    lcp = metrics.get("largest_contentful_paint", {})
    cls = metrics.get("cumulative_layout_shift", {})
    inp = metrics.get("interaction_to_next_paint", {})

    data = {
        "url": results["record"]["key"]["url"],
        "time_to_first_byte_p75": ttfb.get("percentiles", {}).get("p75", None),
        "first_contentful_paint_p75": fcp.get("percentiles", {}).get("p75", None),
        "largest_contentful_paint_p75": lcp.get("percentiles", {}).get("p75", None),
        "cumulative_layout_shift_p75": cls.get("percentiles", {}).get("p75", None),
        "interaction_to_next_paint_p75": inp.get("percentiles", {}).get("p75", None),
    }

    return data


def categorize_histogram(label, histogram):
    data = {}
    if len(histogram) != 3:
        data.update(
            {
                f"{label}_good_density": None,
                f"{label}_needs_improvement_density": None,
                f"{label}_poor_density": None,
            }
        )
    else:
        histogram.sort(key=lambda x: x['start'])

        data.update(
            {
                f"{label}_good_density": histogram[0]["density"],
                f"{label}_needs_improvement_density": histogram[1]["density"],
                f"{label}_poor_density": histogram[2]["density"],
            }
        )

    return dict

if __name__ == "__main__":
    results = {'record': {'key': {'formFactor': 'PHONE', 'url': 'https://www.wikipedia.org/'}, 'metrics': {'first_contentful_paint': {'histogram': [{'start': 0, 'end': 1800, 'density': 0.8874}, {'start': 1800, 'end': 3000, 'density': 0.0729}, {'start': 3000, 'density': 0.0397}], 'percentiles': {'p75': 1126}}, 'first_input_delay': {'histogram': [{'start': 0, 'end': 100, 'density': 0.9797}, {'start': 100, 'end': 300, 'density': 0.0153}, {'start': 300, 'density': 0.005}], 'percentiles': {'p75': 12}}, 'interaction_to_next_paint': {'histogram': [{'start': 0, 'end': 200, 'density': 0.9255}, {'start': 200, 'end': 500, 'density': 0.058}, {'start': 500, 'density': 0.0164}], 'percentiles': {'p75': 104}}, 'largest_contentful_paint': {'histogram': [{'start': 0, 'end': 2500, 'density': 0.927}, {'start': 2500, 'end': 4000, 'density': 0.046}, {'start': 4000, 'density': 0.027}], 'percentiles': {'p75': 1276}}, 'navigation_types': {'fractions': {'navigate_cache': 0.3864, 'reload': 0.0376, 'restore': 0, 'back_forward': 0.0522, 'back_forward_cache': 0.189, 'prerender': 0.0887, 'navigate': 0.2461}}, 'round_trip_time': {'percentiles': {'p75': 144}}, 'cumulative_layout_shift': {'histogram': [{'start': '0.00', 'end': '0.10', 'density': 0.9931}, {'start': '0.10', 'end': '0.25', 'density': 0.0061}, {'start': '0.25', 'density': 0.0008}], 'percentiles': {'p75': '0.00'}}, 'experimental_time_to_first_byte': {'histogram': [{'start': 0, 'end': 800, 'density': 0.8677}, {'start': 800, 'end': 1800, 'density': 0.0893}, {'start': 1800, 'density': 0.043}], 'percentiles': {'p75': 507}}}, 'collectionPeriod': {'firstDate': {'year': 2024, 'month': 8, 'day': 11}, 'lastDate': {'year': 2024, 'month': 9, 'day': 7}}}, 'urlNormalizationDetails': {'originalUrl': 'https://www.wikipedia.org', 'normalizedUrl': 'https://www.wikipedia.org/'}}

    print(format_results(results))

    pass
