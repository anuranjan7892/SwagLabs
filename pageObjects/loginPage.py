from selenium.webdriver.common.by import By

from pageObjects.customSelenium import CustomSelenium
from tests.conftest import get_logger

log = get_logger()


class LoginPage(CustomSelenium):

    USERNAME_FIELD = (By.ID, 'user-name')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD, username)
        log.info(f"Entered username -> {username}")

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)
        log.info(f"Entered password -> {password}")

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)
        log.info("Clicked login button")

    def is_login_button_displayed(self):
        return self.element_displayed(self.LOGIN_BUTTON)

    def login_user(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
