import pytest
from datetime import datetime
from protocol import make_response, make_200, make_404, make_500, validate_request
from resolvers import find_server_actions


@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_action():
    return 'test'

@pytest.fixture
def expected_time():
    return datetime.now().timestamp()

@pytest.fixture
def expected_data():
    return 'some client data'

@pytest.fixture
def initial_request(expected_action, expected_time, expected_data):
    return {
        'action': expected_action,
        'time': expected_time,
        'data': expected_data
    }

@pytest.fixture
def initial_invalid_request(expected_action, expected_time, expected_data):
    return {
        'data': expected_data
    }


def test_action_make_response(initial_request, expected_action, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    action = response.get('action')
    assert action == expected_action


def test_code_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    code = response.get('code')
    assert code == expected_code


def test_time_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    time = response.get('time')
    assert time == expected_time


def test_data_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, date=expected_time)
    data = response.get('data')
    assert data == expected_data


def test_none_request_make_response(expected_code):
    with pytest.raises(AttributeError):
        make_response(None, expected_code)


def test_make_200(initial_request, expected_time):
    response = make_200(initial_request, date=expected_time)
    code = response.get('code')
    assert code == 200


def test_make_404(initial_request, expected_time):
    response = make_404(initial_request, date=expected_time)
    code = response.get('code')
    assert code == 404


def test_make_500(initial_request, expected_time):
    response = make_500(initial_request, date=expected_time)
    code = response.get('code')
    assert code == 500


def test_valid_validate_request(initial_request):
    assert validate_request(initial_request)


def test_invalid_validate_request(initial_invalid_request):
    assert validate_request(initial_invalid_request) == False


def test_find_server_action():
    server_actions = find_server_actions()
    assert type(server_actions) is dict


