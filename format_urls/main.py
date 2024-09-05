"""CLI app to clean the top 10k pages and screens urls for analysis."""

import os
import click
from research.utils.load_results_to_dataframe import load_results_to_dataframe


@click.command()
@click.option(
    "--input-urls",
    "-i",
    required=True,
    type=click.Path(),
    help="Input URL or file containing URLs.",
)
@click.option(
    "--output-file",
    "-o",
    required=True,
    type=click.Path(),
    help="Output file to write responses.",
)
def main(input_urls, output_file):
    """Concatenates domain and page path columns from a CSV file
    into a URL with the https:// protocol prepended."""
    df = load_results_to_dataframe(
        notebook_dir=os.getcwd(),
        file_name=input_urls,
    )
    df["url"] = "https://" + df["domain"] + df["pagePath"]

    df["url"].to_csv(output_file, index=False)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
