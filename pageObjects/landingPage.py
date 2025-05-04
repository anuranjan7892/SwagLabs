import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

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

    def click_add_to_cart(self, item_name):
        by_locator = (By.XPATH, f'//div[div[@class="inventory_item_label"]//div[text()="{item_name}"]]//button[text()="ADD TO CART"]')
        self.click_element(by_locator)
        log.info(f"Clicked on add to cart button for item -> {item_name}")

    def get_item_count_in_shopping_cart(self):
        by_locator = (By.XPATH, "//div[@id='shopping_cart_container']//span[contains(@class, 'shopping_cart_badge')]")
        return self.get_element_text(by_locator)

    def select_sort_by(self, sort_by_option):
        sel = Select(self.get_web_element(self.SORT_DROPDOWN))
        sel.select_by_visible_text(sort_by_option)
        log.info(f"Selected sort by option -> {sort_by_option}")

    def get_items_price_list(self):
        by_locator = (By.CLASS_NAME, "inventory_item_price")
        initial_price_list = self.get_elements_text(by_locator)
        final_price_list = []
        for p in initial_price_list:
            price = re.sub(r'[^\d.]', '', p)
            final_price_list.append(float(price))
        return final_price_list
