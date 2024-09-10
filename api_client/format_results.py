"""
Formats results from CrUX API Response
"""


def format_results(results):
    """Format results for csv file"""
    metrics = results["record"]["metrics"]

    fields = [
        "experimental_time_to_first_byte",
        "first_contentful_paint",
        "largest_contentful_paint",
        "cumulative_layout_shift",
        "interaction_to_next_paint",
    ]

    data = {
        "url": results["record"]["key"]["url"],
    }

    for field in fields:
        data[field + "_p75"] = (
            metrics.get(field, {}).get("percentiles", {}).get("p75", None)
        )
        data.update(
            categorize_histogram(field, metrics.get(field, {}).get("histogram", []))
        )

    return data


def categorize_histogram(label, histogram):
    """Flatten the histogram and divide into good, needs improvement, and poor categories"""
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
        histogram.sort(key=lambda x: x["start"])

        data.update(
            {
                f"{label}_good_density": histogram[0].get("density", None),
                f"{label}_needs_improvement_density": histogram[1].get("density", None),
                f"{label}_poor_density": histogram[2].get("density", None),
            }
        )

    return data


if __name__ == "__main__":
    pass
