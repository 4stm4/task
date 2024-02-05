import pytest
from app import api

test_xml = b'<?xml version="1.0" encoding="UTF-8" ?><data>11</data>'

@pytest.fixture()
def service():
    return api.Extractor()

def test_api_json(service):
    assert service._request_to_data(
        content_type='application/json',
        data=b'{"test": 11}'
    ) == {'test': 11}

def test_api_xml(service):
    assert service._request_to_data(
        content_type='application/xml',
        data=test_xml
    ) == '11'