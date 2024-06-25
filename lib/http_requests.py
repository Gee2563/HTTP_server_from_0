from lib.constants import CRLF

class HTTPRequests:
    def __init__(self, data):
        self.data = data
        self.http_method = None
        self.request_target = None
        self.http_version = None
        self.headers = {}
        self._parse()

    def _parse(self):
        if not self.data:
            raise ValueError('Error with request data')
        lines = self.data.split(f'{CRLF}')
        request_lines = lines[0].split()
        if len(request_lines) != 3 :
            raise ValueError('Error with request data')
        
        self.http_method, self.request_target, self.http_version = request_lines

        i = 1
        while lines[i] != "":
            try:
                key ,value = lines[i].split(": ", 1)
                self.headers[key] = value
                i+= 1
            except ValueError:
                raise ValueError(f'Error with data at line: {lines[i]}')

        if len(lines) > i + 1:
            self.body = lines[i+1]

    def __str__(self) -> str:
        return f"{self.http_method} {self.request_target} {self.http_version}"