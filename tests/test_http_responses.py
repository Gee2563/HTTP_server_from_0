from lib.http_responses import *
import pytest
from lib.http_status_codes import HttpStatusCode
from lib.constants import CRLF

@pytest.fixture
def created_resp():
    http_resp = HttpResponse(200)
    http_resp.add_header('key','value')
    http_resp.write_body('body1')
    return http_resp

def test_attr(created_resp):
    assert created_resp.status_code == 200

def test_add_header(created_resp):
    assert created_resp.headers['key'] == 'value'

def test_write_body(created_resp):
    assert created_resp.body == 'body1'

def test_get_reason_code(created_resp):
    assert created_resp._get_reason_code() == 'OK'

def test_string_format(created_resp):
    assert str(created_resp) == f'HTTP/1.1 200 OK{CRLF}key: value{CRLF}{CRLF}body1'