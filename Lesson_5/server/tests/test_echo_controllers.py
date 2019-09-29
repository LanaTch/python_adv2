from datetime import datetime
from echo.controllers import echo_controller

ACTION = 'test'

CODE = 200

TIME = datetime.now().timestamp()

DATA = 'some client data'
REQUEST = {
    'action': ACTION,
    'time': TIME,
    'data': DATA
}


def test_echo_controller():
    response = echo_controller(REQUEST)
    code = response.get('code')
    assert code == CODE
