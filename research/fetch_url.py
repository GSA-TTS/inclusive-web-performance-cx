import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY_CRUX = os.getenv("GOOGLE_API_KEY_CRUX")

"""
{
  "record": {
    "key": {
      "formFactor": "PHONE",
      "url": "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
    },
    "metrics": {
      "round_trip_time": {
        "percentiles": {
          "p75": 199
        }
      },
      "cumulative_layout_shift": {
        "histogram": [
          {
            "start": "0.00",
            "end": "0.10",
            "density": 0.9474
          },
          {
            "start": "0.10",
            "end": "0.25",
            "density": 0.0381
          },
          {
            "start": "0.25",
            "density": 0.0145
          }
        ],
        "percentiles": {
          "p75": "0.01"
        }
      },
      "experimental_time_to_first_byte": {
        "histogram": [
          {
            "start": 0,
            "end": 800,
            "density": 0.6568
          },
          {
            "start": 800,
            "end": 1800,
            "density": 0.232
          },
          {
            "start": 1800,
            "density": 0.1112
          }
        ],
        "percentiles": {
          "p75": 1133
        }
      },
      "first_contentful_paint": {
        "histogram": [
          {
            "start": 0,
            "end": 1800,
            "density": 0.6226
          },
          {
            "start": 1800,
            "end": 3000,
            "density": 0.089
          },
          {
            "start": 3000,
            "density": 0.2884
          }
        ],
        "percentiles": {
          "p75": 3880
        }
      },
      "first_input_delay": {
        "histogram": [
          {
            "start": 0,
            "end": 100,
            "density": 0.9451
          },
          {
            "start": 100,
            "end": 300,
            "density": 0.047
          },
          {
            "start": 300,
            "density": 0.0079
          }
        ],
        "percentiles": {
          "p75": 11
        }
      },
      "interaction_to_next_paint": {
        "histogram": [
          {
            "start": 0,
            "end": 200,
            "density": 0.767
          },
          {
            "start": 200,
            "end": 500,
            "density": 0.1481
          },
          {
            "start": 500,
            "density": 0.0849
          }
        ],
        "percentiles": {
          "p75": 188
        }
      },
      "largest_contentful_paint": {
        "histogram": [
          {
            "start": 0,
            "end": 2500,
            "density": 0.7034
          },
          {
            "start": 2500,
            "end": 4000,
            "density": 0.0777
          },
          {
            "start": 4000,
            "density": 0.2189
          }
        ],
        "percentiles": {
          "p75": 3316
        }
      },
      "navigation_types": {
        "fractions": {
          "prerender": 0,
          "navigate": 0.4114,
          "navigate_cache": 0.0438,
          "reload": 0.1319,
          "restore": 0,
          "back_forward": 0.0721,
          "back_forward_cache": 0.3408
        }
      }
    },
    "collectionPeriod": {
      "firstDate": {
        "year": 2024,
        "month": 7,
        "day": 27
      },
      "lastDate": {
        "year": 2024,
        "month": 8,
        "day": 23
      }
    }
  }
}
"""


def make_api_request(url):
    api_endpoint = (
        "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key="
        + GOOGLE_API_KEY_CRUX
    )
    payload = {"url": url, "formFactor": "PHONE"}
    response = requests.post(api_endpoint, json=payload)
    return response.json()


res = make_api_request(
    "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
)
print(res)
