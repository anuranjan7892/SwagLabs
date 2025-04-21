from datetime import datetime
import os
from os import path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import yaml

def read_master_config_file():
    """This method is designed to read the master_config file attributes"""
    file_name = path.join(path.dirname(path.dirname(__file__)), 'master_config.yaml')
    stream = open(file_name, 'r')
    data = yaml.safe_load(stream)
    return data

def get_browser_list():
    return read_master_config_file()['BROWSER']

@pytest.fixture(scope='session', params=get_browser_list())
def initialize_driver(request):
    browser = request.param
    browser_name = browser.lower()
    headless = read_master_config_file()['HEADLESS']

    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options = set_headless_browser_options(options, browser_name)
        # To disable Chrome's password manager, as it always pops up for Sauce Demo website
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options = set_headless_browser_options(options, browser_name)
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_name == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options = set_headless_browser_options(options, browser_name)
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    base_url = get_base_url()
    driver.get(base_url)

    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver
    driver.close()
    driver.quit()

def set_headless_browser_options(options, browser):
    if browser == 'chrome':
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
    elif browser == 'firefox':
        options.add_argument("--headless")
    elif browser == 'edge':
        options.add_argument("--headless=new")

    return options

def read_config_file():
    """This method is designed to read the master_config file properties"""
    file_name = path.join(path.dirname(path.dirname(__file__)), 'config.yaml')
    stream = open(file_name, 'r')
    data = yaml.safe_load(stream)
    return data

def get_base_url():
    return read_config_file()['BASE_URL']

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get('initialize_driver', None)
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)

            # create screenshot file name with test name and timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)

            # take screenshot
            driver.save_screenshot(file_path)
            print(f"\n[Screenshot saved to {file_path}]")

            # Attach to Allure report
            with open(file_path, "rb") as file:
                allure.attach(file.read(), name=file_name, attachment_type=allure.attachment_type.PNG)
