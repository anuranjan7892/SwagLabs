from selenium.webdriver.common.by import By

from pageObjects.customSelenium import CustomSelenium


class LandingPage(CustomSelenium):

    APP_LOGO = By.CLASS_NAME, 'app_logos'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def is_logo_present(self):
        return self.element_displayed(self.APP_LOGO)

    def accept_change_password_alert(self):
        self.accept_alert()
