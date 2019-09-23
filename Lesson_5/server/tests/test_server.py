import pytest
from datetime import datetime
from protocol import make_response, make_200, make_404, make_500, validate_request
from resolvers import find_server_actions

ACTION = 'test'

CODE = 200

TIME = datetime.now().timestamp()

DATA = 'some client data'

REQUEST = {
    'action': ACTION,
    'time': TIME,
    'data': DATA
}

RESPONSE = {
    'action': ACTION,
    'time': TIME,
    'code': CODE,
    'data': None
}


def test_action_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('action')
    assert action == ACTION


def test_code_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    code = response.get('code')
    assert code == CODE


def test_time_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    time = response.get('time')
    assert time == TIME


def test_data_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    data = response.get('data')
    assert data == DATA


def test_none_request_make_response():
    with pytest.raises(AttributeError):
        make_response(None, CODE)


def test_make_200():
    response = make_200(REQUEST, date=TIME)
    code = response.get('code')
    assert code == 200


def test_make_404():
    response = make_404(REQUEST, date=TIME)
    code = response.get('code')
    assert code == 404


def test_make_500():
    response = make_500(REQUEST, date=TIME)
    code = response.get('code')
    assert code == 500


def test_validate_request():
    response = validate_request(REQUEST)
    assert response


def test_find_server_action():
    server_actions = find_server_actions()
    assert type(server_actions) is dict


