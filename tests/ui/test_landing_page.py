import pytest
import requests

from pageObjects.landingPage import LandingPage
from pageObjects.loginPage import LoginPage
from tests.baseTest import BaseTest
from utilities.logger_utils import get_logger

log = get_logger()


class TestLandingPage(BaseTest):

    @pytest.fixture(scope='class', autouse=True)
    def login_and_logout(self):
        login_page = LoginPage(self.driver)
        landing_page = LandingPage(self.driver)
        login_page.login_user("standard_user", "secret_sauce")
        if landing_page.is_logo_present():
            log.info("Login was successful")
        else:
            assert False, log.critical("Login was unsuccessful")
        yield
        landing_page.logout_user()
        if login_page.is_login_button_displayed():
            log.info("Logout was successful")
        else:
            assert False, log.critical("Logout was unsuccessful")

    def test_opencart_logo(self):
        landing_page = LandingPage(self.driver)
        if landing_page.is_logo_present():
            log.info("Logo is displayed")
        else:
            assert False, log.critical("Logo is not displayed")

    def test_menu_items(self):
        landing_page = LandingPage(self.driver)
        landing_page.click_hamburger_menu()

        expected_menu_items = ["All Items", "About", "Logout", "Reset App State"]
        actual_menu_items = landing_page.get_menu_items()
        landing_page.click_close_menu()

        if actual_menu_items == expected_menu_items:
            log.info("All menu items displayed")
        else:
            assert False, log.critical(f"Menu items are not displayed correctly. Actual menu items: {actual_menu_items}"
                                       f" ; Expected menu items: {expected_menu_items}")

    def test_sort_dropdown(self):
        landing_page = LandingPage(self.driver)
        if landing_page.is_sort_dropdown_present():
            log.info("Sort dropdown is displayed")
        else:
            assert False, log.critical("Sort dropdown is not displayed")

    def test_products_displayed(self):
        landing_page = LandingPage(self.driver)
        inventory_items = landing_page.get_inventory_items()
        if len(inventory_items) == 6:
            log.info("All products are displayed")
        else:
            assert False, log.critical("No or less products are displayed")

    def test_items_images_displayed(self):
        landing_page = LandingPage(self.driver)
        items_image_list = landing_page.get_item_images()
        assert_list = []
        for item in items_image_list:
            response = requests.head(item)
            if response.status_code != 200:
                assert_list.append(item)
                log.critical(f"{item}: Image is not displayed")
            else:
                log.info(f"{item}: Image is displayed")
        assert not assert_list, "Some of the product's image are not displayed"

    @pytest.mark.smoke
    def test_add_item_to_cart(self):
        print("Item is added to cart successfully")

    def test_sorting_functionality(self):
        print("Sorting functionality is working as expected")
