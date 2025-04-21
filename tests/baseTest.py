import pytest


@pytest.mark.usefixtures("initialize_driver", "logger")
class BaseTest:
    pass
