from lib.constants import CRLF
from lib.HTTP_header_names import HTTPHeaderNames
from lib.http_status_codes import HttpStatusCode

class HttpResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.headers = {}
        self.body = None
        self.http_version = "HTTP/1.1"
    
    def add_header(self,key,value):
        self.headers[key] = value
    
    def write_body(self,body):
        self.body = body

    def _get_reason_code(self):
        return {
            HttpStatusCode.OK: "OK",
            HttpStatusCode.NOT_FOUND: "Not Found",
        }.get(self.status_code, "Unknown")

    def __str__(self) -> str:
        status_line = f'{self.http_version} {self.status_code} {self._get_reason_code()}'
        header = (CRLF).join(f"{key}: {self.headers[key]}" for key in self.headers)
        response = f"{status_line}{CRLF}{header}{CRLF}{CRLF}"
        if self.body:
            response += self.body
        return response