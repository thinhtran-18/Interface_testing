"""Shared browser actions; extend only when the team has repeated needs."""

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
