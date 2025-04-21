from selenium.webdriver.common.by import By

from pageObjects.customSelenium import CustomSelenium
from tests.conftest import get_logger

log = get_logger()

class LandingPage(CustomSelenium):

    APP_LOGO = By.CLASS_NAME, 'app_logo'
    HAMBURGER_MENU = By.XPATH, "//button[text()='Open Menu']"
    LOGOUT_LINK = By.ID, 'logout_sidebar_link'
    CLOSE_MENU = By.XPATH, "//button[text()='Close Menu']"
    SORT_DROPDOWN = By.CLASS_NAME, "product_sort_container"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def is_logo_present(self):
        return self.element_displayed(self.APP_LOGO)

    def click_hamburger_menu(self):
        self.click_element(self.HAMBURGER_MENU)
        log.info("Clicked on hamburger menu")

    def click_logout(self):
        self.click_element(self.LOGOUT_LINK)
        log.info("Clicked on logout")

    def logout_user(self):
        self.click_hamburger_menu()
        self.click_logout()

    def get_menu_items(self):
        by_locator = (By.XPATH, "//a[contains(@id,'_sidebar_link')]")
        return self.get_elements_text(by_locator)

    def click_close_menu(self):
        self.click_element(self.CLOSE_MENU)
        log.info("Clicked on close menu")

    def is_sort_dropdown_present(self):
        return self.element_displayed(self.SORT_DROPDOWN)

    def get_inventory_items(self):
        by_locator = (By.XPATH, "//div[@class='inventory_item']")
        return self.get_web_elements(by_locator)

    def get_item_images(self):
        by_locator = (By.XPATH, "//img[@class='inventory_item_img']")
        els = self.get_web_elements(by_locator)
        images_list = []
        for el in els:
            images_list.append(el.get_attribute('src'))
        return images_list
