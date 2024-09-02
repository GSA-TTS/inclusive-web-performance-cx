"""API client for the CrUX API."""

import requests


class CruxAPIException(Exception):
    """Base exception class for CruxAPI errors"""

    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class BadRequestException(CruxAPIException):
    """Exception raised for a 400 Bad Request response"""


class UnauthorizedException(CruxAPIException):
    """Exception raised for a 401 Unauthorized response"""


class ForbiddenException(CruxAPIException):
    """Exception raised for a 403 Forbidden response"""


class NotFoundException(CruxAPIException):
    """Exception raised for a 404 Not Found response"""


class InternalServerErrorException(CruxAPIException):
    """Exception raised for a 500 Internal Server Error response"""


class UnknownAPIException(CruxAPIException):
    """Exception raised for a 500 Internal Server Error response"""


class CruxAPIClient:
    """Makes a CrUX API request for a URL or origin."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_base_url = "https://chromeuxreport.googleapis.com"
        self.api_version = "v1"
        self.api_route = "records:queryRecord"
        self.api_endpoint = (
            f"{self.api_base_url}/{self.api_version}/"
            f"{self.api_route}?key={self.api_key}"
        )

    def get_url(self, url: str, params: dict = None, headers: dict = None):
        """Calls the CrUX API for a single URL"""
        payload = {"url": url}
        headers = {"Content-Type": "application/json"}

        if params:
            payload.update(params)

        if headers:
            headers.update(headers)

        response = requests.post(
            self.api_endpoint, json=payload, headers=headers, timeout=10
        )
        return self._handle_response(response)

    def get_origin(self, origin, params: dict = None, headers: dict = None):
        """Calls the CrUX API for an origin"""
        payload = {"origin": origin}
        headers = {"Content-Type": "application/json"}

        if params:
            payload.update(params)

        if headers:
            headers.update(headers)

        response = requests.post(
            self.api_endpoint, json=payload, headers=headers, timeout=10
        )
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        """Handle the HTTP response errors."""
        if response.status_code == 200:
            return response.json()
        if response.status_code == 400:
            raise BadRequestException("Bad Request", status_code=response.status_code)
        if response.status_code == 401:
            raise UnauthorizedException(
                "Unauthorized", status_code=response.status_code
            )
        if response.status_code == 403:
            raise ForbiddenException("Forbidden", status_code=response.status_code)
        if response.status_code == 404:
            raise NotFoundException("Not Found", status_code=response.status_code)
        if response.status_code == 500:
            raise InternalServerErrorException(
                "Internal Server Error", status_code=response.status_code
            )

        raise UnknownAPIException(
            "An unknown error occurred.", status_code=response.status_code
        )
