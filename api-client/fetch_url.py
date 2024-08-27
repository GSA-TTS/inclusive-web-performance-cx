import os
from research.utils.load_results_to_dataframe import load_results_to_dataframe
import requests
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GOOGLE_API_KEY_CRUX = os.getenv("GOOGLE_API_KEY_CRUX")

# Read the CSV file
df = load_results_to_dataframe(
    notebook_dir=os.getcwd(),
    file_name="../research/data/top-10000-pages-and-screens-30-days-20240812.csv"
)

df = df.head(1000)
df["url"] = "https://" + df["domain"] + df["pagePath"]

# Initialize the token bucket
RATE_LIMIT = 5  # Number of tokens (API requests) per minute
REFILL_TIME = 10  # Time in seconds to refill the tokens
tokens = RATE_LIMIT
last_request_time = time.time()


def get_tokens():
    global tokens, last_request_time
    current_time = time.time()
    time_passed = current_time - last_request_time
    # Calculate how many tokens should be added
    tokens_to_add = int(time_passed / REFILL_TIME * RATE_LIMIT)
    tokens = min(RATE_LIMIT, tokens + tokens_to_add)
    last_request_time = current_time


def make_api_request(url):
    api_endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=" + GOOGLE_API_KEY_CRUX
    payload = {
        "url": url,
        "formFactor": "PHONE"
    }
    response = requests.post(api_endpoint, json=payload)
    return response.json()


# Iterate through each URL
for index, row in df.iterrows():
    get_tokens()

    if tokens > 0:
        # Use a token
        tokens -= 1

        # Get the URL from the CSV
        url = row['url']
        print(url)

        try:
            # Make API request
            response_data = make_api_request(url)

            print(response_data)

            # Extract the relevant data from the response
            # Example: Assuming we're extracting 'first_contentful_paint'
            time_to_first_byte = response_data['record']['metrics']['experimental_time_to_first_byte']['percentiles']['p75']
            first_contentful_paint = response_data['record']['metrics']['first_contentful_paint']['percentiles']['p75']
            largest_contentful_paint = response_data['record']['metrics']['largest_contentful_paint']['percentiles']['p75']
            cumulative_layout_shift = response_data['record']['metrics']['cumulative_layout_shift']['percentiles']['p75']
            interaction_to_next_paint = response_data['record']['metrics']['interaction_to_next_paint']['percentiles']['p75']

            # Update the DataFrame with the relevant data
            df.at[index, 'time_to_first_byte'] = time_to_first_byte
            df.at[index, 'first_contentful_paint'] = first_contentful_paint
            df.at[index, 'largest_contentful_paint'] = largest_contentful_paint
            df.at[index, 'cumulative_layout_shift'] = cumulative_layout_shift
            df.at[index, 'interaction_to_next_paint'] = interaction_to_next_paint

        except Exception as e:
            print(f"Failed to fetch data for {url}: {e}")

    else:
        print("Rate limit reached. Waiting...")
        time.sleep(REFILL_TIME)  # Wait for the token bucket to refill

# Save the updated DataFrame back to the CSV file
df.to_csv('top-1k-crux-20240826.csv', index=False)

# import os
# import requests
# from dotenv import load_dotenv
#
# load_dotenv()
#
# GOOGLE_API_KEY_CRUX = os.getenv("GOOGLE_API_KEY_CRUX")
#
# """
# {
#   "record": {
#     "key": {
#       "formFactor": "PHONE",
#       "url": "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
#     },
#     "metrics": {
#       "round_trip_time": {
#         "percentiles": {
#           "p75": 199
#         }
#       },
#       "cumulative_layout_shift": {
#         "histogram": [
#           {
#             "start": "0.00",
#             "end": "0.10",
#             "density": 0.9474
#           },
#           {
#             "start": "0.10",
#             "end": "0.25",
#             "density": 0.0381
#           },
#           {
#             "start": "0.25",
#             "density": 0.0145
#           }
#         ],
#         "percentiles": {
#           "p75": "0.01"
#         }
#       },
#       "experimental_time_to_first_byte": {
#         "histogram": [
#           {
#             "start": 0,
#             "end": 800,
#             "density": 0.6568
#           },
#           {
#             "start": 800,
#             "end": 1800,
#             "density": 0.232
#           },
#           {
#             "start": 1800,
#             "density": 0.1112
#           }
#         ],
#         "percentiles": {
#           "p75": 1133
#         }
#       },
#       "first_contentful_paint": {
#         "histogram": [
#           {
#             "start": 0,
#             "end": 1800,
#             "density": 0.6226
#           },
#           {
#             "start": 1800,
#             "end": 3000,
#             "density": 0.089
#           },
#           {
#             "start": 3000,
#             "density": 0.2884
#           }
#         ],
#         "percentiles": {
#           "p75": 3880
#         }
#       },
#       "first_input_delay": {
#         "histogram": [
#           {
#             "start": 0,
#             "end": 100,
#             "density": 0.9451
#           },
#           {
#             "start": 100,
#             "end": 300,
#             "density": 0.047
#           },
#           {
#             "start": 300,
#             "density": 0.0079
#           }
#         ],
#         "percentiles": {
#           "p75": 11
#         }
#       },
#       "interaction_to_next_paint": {
#         "histogram": [
#           {
#             "start": 0,
#             "end": 200,
#             "density": 0.767
#           },
#           {
#             "start": 200,
#             "end": 500,
#             "density": 0.1481
#           },
#           {
#             "start": 500,
#             "density": 0.0849
#           }
#         ],
#         "percentiles": {
#           "p75": 188
#         }
#       },
#       "largest_contentful_paint": {
#         "histogram": [
#           {
#             "start": 0,
#             "end": 2500,
#             "density": 0.7034
#           },
#           {
#             "start": 2500,
#             "end": 4000,
#             "density": 0.0777
#           },
#           {
#             "start": 4000,
#             "density": 0.2189
#           }
#         ],
#         "percentiles": {
#           "p75": 3316
#         }
#       },
#       "navigation_types": {
#         "fractions": {
#           "prerender": 0,
#           "navigate": 0.4114,
#           "navigate_cache": 0.0438,
#           "reload": 0.1319,
#           "restore": 0,
#           "back_forward": 0.0721,
#           "back_forward_cache": 0.3408
#         }
#       }
#     },
#     "collectionPeriod": {
#       "firstDate": {
#         "year": 2024,
#         "month": 7,
#         "day": 27
#       },
#       "lastDate": {
#         "year": 2024,
#         "month": 8,
#         "day": 23
#       }
#     }
#   }
# }
# """
