import os
from dotenv import load_dotenv, find_dotenv
from research.utils.load_results_to_dataframe import load_results_to_dataframe
from crux_api_client import CruxAPIClient
from token_bucket import TokenBucket

load_dotenv(find_dotenv())

GOOGLE_API_KEY_CRUX = os.getenv("GOOGLE_API_KEY_CRUX")


def update_dataframe_with_response(df, index, response_data):
    try:
        metrics = response_data["record"]["metrics"]
        df.at[index, "time_to_first_byte"] = metrics["experimental_time_to_first_byte"][
            "percentiles"
        ]["p75"]
        df.at[index, "first_contentful_paint"] = metrics["first_contentful_paint"][
            "percentiles"
        ]["p75"]
        df.at[index, "largest_contentful_paint"] = metrics["largest_contentful_paint"][
            "percentiles"
        ]["p75"]
        df.at[index, "cumulative_layout_shift"] = metrics["cumulative_layout_shift"][
            "percentiles"
        ]["p75"]
        df.at[index, "interaction_to_next_paint"] = metrics[
            "interaction_to_next_paint"
        ]["percentiles"]["p75"]
    except KeyError as e:
        print(f"KeyError: {e} in response data for index {index}")


def main(df, output):
    # Initialize the API client
    token_bucket = TokenBucket(rate_limit=8, refill_time=5)
    crux_api_client = CruxAPIClient(GOOGLE_API_KEY_CRUX)

    # Iterate through each URL
    for index, row in df.iterrows():
        url = row["url"]
        print(f"{index} - Fetching data for {url}")
        try:
            response_data = token_bucket.execute(
                crux_api_client.get_url(
                    url,
                    {
                        "formFactor": "PHONE",
                    },
                )
            )
            print(response_data)
            if response_data.get("record") is None:
                continue
            else:
                update_dataframe_with_response(df, index, response_data)
                # Save the updated row to the CSV file after each API call
                df.iloc[[index]].to_csv(
                    output, mode="a", header=not os.path.exists(output), index=False
                )
        except Exception as e:
            print(f"Failed to fetch data for {url}: {e}")


if __name__ == "__main__":
    # Load the CSV file into a DataFrame
    df = load_results_to_dataframe(
        notebook_dir=os.getcwd(),
        file_name="../research/data/top-10000-pages-and-screens-30-days-20240828.csv",
    )
    # df = df.sample(frac=0.25, replace=False).reset_index(drop=True)
    df["url"] = "https://" + df["domain"] + df["pagePath"]

    df["url"].to_csv("result.txt", index=False)

    # main(df, "sampled-crux-data-20240828.csv")
