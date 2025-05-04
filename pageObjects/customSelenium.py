from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from tests.conftest import get_logger

log = get_logger()

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
            log.critical(f"Wait for element timed out, locator -> {locator} : Exception -> {e}")
            el = self.driver.find_element(*locator)
        except NoSuchElementException as e:
            log.critical(f"Element not found, locator -> {locator} : Exception -> {e}")
            el = None
        return el

    def click_element(self, locator):
        """Attempts to click an element, with retries for visibility and stale element cases."""
        try:
            el = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator))
            el.click()
            return
        except (TimeoutException, StaleElementReferenceException) as e:
            log.warning(f"Initial click failed for locator -> {locator} : Exception -> {e}. Retrying...")

        # Retry with JavaScript click as a fallback
        try:
            el = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", el)
            log.info(f"Clicked element via JavaScript fallback: {locator}")
        except Exception as final_exception:
            log.critical(f"Final click attempt failed for locator -> {locator} : Exception -> {final_exception}")
            raise  # Optionally re-raise if failure should stop the test

    def enter_text(self, locator, text):
        try:
            el = self.get_web_element(locator)
            el.send_keys(text)
        except StaleElementReferenceException as e:
            log.critical(f"Stale element reference, locator -> {locator} : Exception -> {e}")

    def element_displayed(self, locator):
        try:
            el = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(locator))
            return el.is_displayed()
        except TimeoutException as e:
            log.critical(f"Element is not displayed, locator -> {locator} : Exception -> {e}")
            return False

    def get_element_text(self, locator):
        el = self.get_web_element(locator)
        return el.text if el else None

    def wait_for_alert(self):
        try:
            WebDriverWait(self.driver, 10).until(ec.alert_is_present())
        except TimeoutException as e:
            log.critical(f"Alert is not displayed, Exception -> {e}")

    def accept_alert(self):
        try:
            self.wait_for_alert()
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            log.critical(f"Alert is not displayed, Exception -> {e}")

    def get_web_elements(self, by_locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(by_locator))
        except TimeoutException:
            log.error(f"Elements not found for locator: {by_locator} within {timeout} seconds")
            return []

    def get_elements_text(self, by_locator):
        text_list = []
        els = self.get_web_elements(by_locator)
        for el in els:
            text_list.append(el.text)
        return text_list

    def get_element_attribute(self, by_locator, attribute):
        el = self.get_web_element(by_locator)
        return el.get_attribute(attribute)

    def click_element_using_javascript_executor(self, locator):
        el = self.get_web_element(locator)
        self.driver.execute_script("arguments[0].click();", el)
