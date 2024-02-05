import pytest
from app import Normalizer

@pytest.fixture(scope='function')
def service():
    return Normalizer()

def test_get_digit1(service):
    assert service._get_digit('одинадцать') == 11

def test_get_digit2(service):
    assert service._get_digit('сорок') == 40

def test_fail_get_digit(service):
    assert service._get_digit('в течении') == 0

def test_fail_get_month(service):
    assert service._get_month('фезраль') == ''

def test_get_month1(service):
    assert service._get_month('январь') == '01'

def test_get_month2(service):
    assert service._get_month('Ноябрь') == '11'

def test_get_period(service):
    assert service._get_period('неделя') == 2

def test_fail_get_period(service):
    assert service._get_period('year') == -1

def test_period(service):
    assert service.period('тридцать три года 11 месяцев семнадцать недель четверо суток') == '33_11_17_4'

def test_period(service):
    assert service.period('в течении полугода и трёх дней') == '0_6_0_3'

def test_date(service):
    assert service.date('14 янв. 2018 год.') == '14.01.2018'

def test_date2(service):
    assert service.date('третье сентября 2023 года') == '03.09.2023'