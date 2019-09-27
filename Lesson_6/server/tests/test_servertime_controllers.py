from servertime.controllers import timestamp_controller


REQUEST = {}


def test_errors_controller():
    response = timestamp_controller(REQUEST)
    time = response.get('time')
    assert type(time) is float
