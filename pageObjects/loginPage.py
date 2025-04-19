from selenium.webdriver.common.by import By

from pageObjects.customSelenium import CustomSelenium


class LoginPage(CustomSelenium):

    USERNAME_FIELD = (By.ID, 'user-name')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)
