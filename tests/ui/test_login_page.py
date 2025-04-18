import pytest


class TestLoginPage:

    @pytest.mark.smoke
    def test_login_functionality(self):
        print("User should be able to login successfully")

    @pytest.mark.smoke
    def test_logout_functionality(self):
        print("User should be able to logout successfully")