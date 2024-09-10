"""CLI for running a list of urls through the Chrome User Experience Report API"""

import csv
import os

import click
from dotenv import load_dotenv, find_dotenv

from api_client.format_results import format_results
from api_client.crux_api_client import CruxAPIClient, NotFoundException
from api_client.token_bucket import TokenBucket

load_dotenv(find_dotenv())


@click.command()
@click.option(
    "--input-urls", "-i", required=True, help="Input URL or file containing URLs."
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(),
    help="Output file to write responses (prints to console if not provided).",
)
@click.option(
    "--api-key",
    "-k",
    default=os.getenv("GOOGLE_API_KEY_CRUX"),
    help="API key for requests (reads from .env if not provided).",
)
@click.option(
    "--threshold",
    "-t",
    default=10,
    type=int,
    help="Stop after {x} consecutive errors",
)
def main(input_urls, output_file, api_key, threshold):
    """
    CLI tool to fetch URLs from a file or CLI arg and save or print the responses.
    """
    if not api_key:
        click.echo("API key is required. Provide it via --api-key or in a .env file.")
        return

    token_bucket = TokenBucket(rate_limit=10, refill_time=5)
    crux_api_client = CruxAPIClient(api_key)

    # Determine if input_urls is a single URL or a file
    if os.path.exists(input_urls):
        with open(input_urls, "r", encoding="utf8") as infile:
            urls = infile.read().splitlines()
    else:
        urls = [input_urls]

    needs_header = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

    error_count = 0

    # Fetch each URL
    for index, url in enumerate(urls):
        click.echo(f"{index} - Fetching data for {url}")
        try:
            response_data = token_bucket.execute(
                crux_api_client.get_url(
                    url,
                    {
                        "formFactor": "PHONE",
                    },
                )
            )
            if response_data.get("record") is None:
                continue

            if output_file:
                click.echo(response_data)
                formatted_results = format_results(response_data)
                with open(output_file, mode="a", newline="", encoding="utf8") as file:
                    writer = csv.writer(file)
                    if needs_header:
                        writer.writerow(list(formatted_results.keys()))
                        needs_header = False
                    writer.writerow(list(formatted_results.values()))
            else:
                click.echo(response_data)

            error_count = 0

        except NotFoundException as e:
            error_count += 1
            click.echo(f"Failed to fetch {url}: {e}")

        if error_count >= threshold:
            break


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
