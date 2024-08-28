import os
import time
import requests

class CruxAPIClient:
    def __init__(self, rate_limit, refill_time):
        self.rate_limit = rate_limit
        self.refill_time = refill_time
        self.tokens = rate_limit
        self.last_request_time = time.time()

    def get_tokens(self):
        current_time = time.time()
        time_passed = current_time - self.last_request_time
        tokens_to_add = int(time_passed / self.refill_time * self.rate_limit)
        self.tokens = min(self.rate_limit, self.tokens + tokens_to_add)
        self.last_request_time = current_time

    def make_api_request(self, endpoint, url):
        self.get_tokens()

        if self.tokens > 0:
            self.tokens -= 1
            api_endpoint = endpoint
            payload = {
                "url": url,
                "formFactor": "PHONE"
            }
            response = requests.post(api_endpoint, json=payload)
            return response.json()

        else:
            time.sleep(self.refill_time)
            return self.make_api_request(url)
