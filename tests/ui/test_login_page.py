import pytest

from pageObjects.landingPage import LandingPage
from pageObjects.loginPage import LoginPage
from tests.baseTest import BaseTest


class TestLoginPage(BaseTest):

    def test_login_functionality(self):
        print("User should be able to login successfully")
        login_page = LoginPage(self.driver)
        landing_page = LandingPage(self.driver)

        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.click_login()

        assert landing_page.is_logo_present(), "Login unsuccessful"

    @pytest.mark.smoke
    def test_logout_functionality(self):
        print("User should be able to logout successfully")
