import pytest
from servererrors.controllers import errors_controller


REQUEST = {}


def test_errors_controller():
    with pytest.raises(Exception):
        errors_controller(REQUEST)
