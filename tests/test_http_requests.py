import unittest
import pytest

from lib.constants import CRLF
from lib.http_requests import HTTPRequests

class HTTPRequestsTests(unittest.TestCase):
    @staticmethod
    def test_valid_http_request():
        data = f"GET /index.html HTTP/1.1{CRLF}Host: example.com{CRLF}User-Agent: Mozilla/5.0{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.http_method == "GET"
        assert request.request_target == "/index.html"
        assert request.http_version == "HTTP/1.1"
        assert request.headers == {"Host": "example.com", "User-Agent": "Mozilla/5.0"}
        assert str(request) == "GET /index.html HTTP/1.1"
    @staticmethod
    def test_valid_http_request_no_headers():
        data = f"POST /submit HTTP/1.1{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.http_method == "POST"
        assert request.request_target == "/submit"
        assert request.http_version == "HTTP/1.1"
        assert request.headers == {}
    @staticmethod
    def test_valid_http_request_multiple_headers():
        data = (
            f"PUT /update HTTP/1.1{CRLF}Content-Type: application/json{CRLF}Authorization: Bearer token{CRLF}"
            f"Content-Length: 100{CRLF}{CRLF}"
        )
        request = HTTPRequests(data)
        assert request.http_method == "PUT"
        assert request.request_target == "/update"
        assert request.http_version == "HTTP/1.1"
        assert request.headers == {
            "Content-Type": "application/json",
            "Authorization": "Bearer token",
            "Content-Length": "100",
        }
    @staticmethod
    def test_invalid_request_line():
        data = f"GET /index.html{CRLF}Host: example.com{CRLF}{CRLF}"
        with pytest.raises(ValueError, match="Error with request data"):
            HTTPRequests(data)
    @staticmethod
    def test_malformed_header():
        data = f"GET /index.html HTTP/1.1{CRLF}Invalid-Header{CRLF}{CRLF}"
        with pytest.raises(ValueError, match="Error with data at line: Invalid-Header"):
            HTTPRequests(data)
    @staticmethod
    def test_empty_request():
        data = ""
        with pytest.raises(ValueError, match="Error with request data"):
            HTTPRequests(data)
    @staticmethod
    def test_request_with_body():
        body = "name=John&age=30"
        data = (
            f"POST /submit HTTP/1.1{CRLF}Content-Type: application/x-www-form-urlencoded{CRLF}"
            f"Content-Length: {len(body)}{CRLF}{CRLF}{body}"
        )
        request = HTTPRequests(data)
        assert request.http_method == "POST"
        assert request.request_target == "/submit"
        assert request.http_version == "HTTP/1.1"
        assert request.headers == {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(body)),
        }
    @staticmethod
    def test_case_sensitive_headers():
        data = f"GET /index.html HTTP/1.1{CRLF}Host: example.com{CRLF}USER-AGENT: Mozilla/5.0{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.headers == {"Host": "example.com", "USER-AGENT": "Mozilla/5.0"}
    @staticmethod
    def test_http_version_variations():
        data = f"GET /index.html HTTP/2{CRLF}Host: example.com{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.http_version == "HTTP/2"
    @staticmethod
    def test_request_target_variations():
        data = f"GET http://example.com/index.html HTTP/1.1{CRLF}Host: example.com{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.request_target == "http://example.com/index.html"
    @staticmethod
    def test_header_with_multiple_colons():
        data = f"GET /index.html HTTP/1.1{CRLF}Host: example.com{CRLF}Custom-Header: value: with: colons{CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.headers["Custom-Header"] == "value: with: colons"
    @staticmethod
    def test_header_with_leading_trailing_spaces():
        data = f"GET /index.html HTTP/1.1{CRLF}Host:  example.com  {CRLF}User-Agent:  Mozilla/5.0  {CRLF}{CRLF}"
        request = HTTPRequests(data)
        assert request.headers == {
            "Host": " example.com  ",
            "User-Agent": " Mozilla/5.0  ",
        }

if __name__ == "__main__":
    unittest.main()