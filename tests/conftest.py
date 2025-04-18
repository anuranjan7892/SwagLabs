from os import path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import yaml

@pytest.fixture(scope='session')
def initialize_driver(browser):

    headless = read_master_comfig_file()['headless']

    if browser.lower == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options = set_headless_browser_options(options, browser)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser.lower == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options = set_headless_browser_options(options, browser)
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser.lower == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options = set_headless_browser_options(options, browser)
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(2)

    yield driver
    driver.close()
    driver.quit()

def set_headless_browser_options(options, browser):
    if browser.lower == 'chrome':
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    elif browser.lower == 'firefox':
        options.add_argument("--headless")
    elif browser.lower == 'edge':
        options.add_argument("--headless=new")

    return options

def read_master_comfig_file():
    """This method is designed to read the master_config file properties"""
    file_name = path.join(path.dirname(path.dirname(__file__)), 'master_config.yaml')
    stream = open(file_name, 'r')
    data = yaml.safe_load(stream)
    return data






