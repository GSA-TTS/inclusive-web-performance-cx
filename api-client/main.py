import os
from dotenv import load_dotenv, find_dotenv
from research.utils.load_results_to_dataframe import load_results_to_dataframe
from crux_api_client import CruxAPIClient

load_dotenv(find_dotenv())

GOOGLE_API_KEY_CRUX = os.getenv("GOOGLE_API_KEY_CRUX")


def update_dataframe_with_response(df, index, response_data):
    try:
        metrics = response_data['record']['metrics']
        df.at[index, 'time_to_first_byte'] = metrics['experimental_time_to_first_byte']['percentiles']['p75']
        df.at[index, 'first_contentful_paint'] = metrics['first_contentful_paint']['percentiles']['p75']
        df.at[index, 'largest_contentful_paint'] = metrics['largest_contentful_paint']['percentiles']['p75']
        df.at[index, 'cumulative_layout_shift'] = metrics['cumulative_layout_shift']['percentiles']['p75']
        df.at[index, 'interaction_to_next_paint'] = metrics['interaction_to_next_paint']['percentiles']['p75']
    except KeyError as e:
        print(f"KeyError: {e} in response data for index {index}")

def main(df, output):
    # Initialize the API client
    crux_client = CruxAPIClient(rate_limit=5, refill_time=6)

    # Iterate through each URL
    for index, row in df.iterrows():
        url = row['url']
        print(f"Fetching data for {url}")
        try:
            response_data = crux_client.make_api_request(f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={GOOGLE_API_KEY_CRUX}", url)
            if response_data.get('record') is None:
                continue
            else:
                print(response_data)
                update_dataframe_with_response(df, index, response_data)
                # Save the updated row to the CSV file after each API call
                df.iloc[[index]].to_csv(output, mode='a', header=not os.path.exists(output), index=False)
        except Exception as e:
            print(f"Failed to fetch data for {url}: {e}")


if __name__ == "__main__":
    # Load the CSV file into a DataFrame
    df = load_results_to_dataframe(
        notebook_dir=os.getcwd(),
        file_name="../research/data/top-10000-pages-and-screens-30-days-20240812.csv"
    )
    df = df.sample(frac=0.2, replace=False).reset_index(drop=True)
    df["url"] = "https://" + df["domain"] + df["pagePath"]

    main(df, 'sampled-crux-random-2k-20240828.csv')
