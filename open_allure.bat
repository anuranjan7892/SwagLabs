@echo off
echo Running tests and generating Allure report...
pytest -k "test_login_functionality"
allure serve allure-results