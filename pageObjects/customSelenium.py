from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class CustomSelenium:

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def get_web_element(self, locator):
        try:
            el = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(locator))
        except TimeoutException as e:
            print(f"Wait for element timed out, locator -> {locator} : Exception -> {e}")
            el = self.driver.find_element(*locator)
        except NoSuchElementException as e:
            print(f"Element not found, locator -> {locator} : Exception -> {e}")
            el = None
        return el

    def click_element(self, locator):
        try:
            el = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator))
            el.click()
        except TimeoutException as e:
            print(f"Wait for element timed out, locator -> {locator} : Exception -> {e}")
        except StaleElementReferenceException as e:
            print(f"Stale element reference, locator -> {locator} : Exception -> {e}")

    def enter_text(self, locator, text):
        try:
            el = self.get_web_element(locator)
            el.send_keys(text)
        except StaleElementReferenceException as e:
            print(f"Stale element reference, locator -> {locator} : Exception -> {e}")

    def element_displayed(self, locator):
        try:
            el = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(locator))
            return el.is_displayed()
        except TimeoutException as e:
            print(f"Element is not displayed, locator -> {locator} : Exception -> {e}")
            return False

    def wait_for_alert(self):
        try:
            WebDriverWait(self.driver, 10).until(ec.alert_is_present())
        except TimeoutException as e:
            print(f"Alert is not displayed, Exception -> {e}")

    def accept_alert(self):
        try:
            self.wait_for_alert()
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            print(f"Alert is not displayed, Exception -> {e}")
