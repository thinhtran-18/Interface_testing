"""Page Object for SSO Login page with form interactions and validation support."""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "Username")
    PASSWORD_INPUT = (By.ID, "Password")
    REMEMBER_CHECKBOX = (By.ID, "RememberLogin")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.btn-login, button[type='submit']")
    EYE_TOGGLE = (By.CSS_SELECTOR, "a.toggle-password")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")
    ERROR_SUMMARY = (By.CSS_SELECTOR, ".validation-summary-errors")
    FORGOT_PASSWORD_LINK = (By.PARTIAL_LINK_TEXT, "Quên mật khẩu")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self) -> bool:
        """Wait until on SSO login page and form is ready."""
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        return True

    def enter_username(self, username: str) -> None:
        elem = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        elem.clear()
        if username:
            elem.send_keys(username)

    def enter_password(self, password: str) -> None:
        elem = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        elem.clear()
        if password:
            elem.send_keys(password)

    def click_login(self) -> None:
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def login(self, username: str, password: str) -> None:
        """Perform full login action."""
        self.is_loaded()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_password_input_type(self) -> str:
        elem = self.driver.find_element(*self.PASSWORD_INPUT)
        return elem.get_attribute("type")

    def toggle_password_visibility(self) -> None:
        toggle = self.wait.until(EC.presence_of_element_located(self.EYE_TOGGLE))
        self.driver.execute_script("arguments[0].click();", toggle)

    def is_remember_checked(self) -> bool:
        checkbox = self.driver.find_element(*self.REMEMBER_CHECKBOX)
        return checkbox.is_selected()

    def toggle_remember(self) -> None:
        checkbox = self.wait.until(EC.presence_of_element_located(self.REMEMBER_CHECKBOX))
        self.driver.execute_script("arguments[0].click();", checkbox)

    def get_error_message(self) -> str:
        """Wait for and get validation or alert error message text."""
        alert = self.wait.until(EC.visibility_of_element_located(self.ERROR_ALERT))
        return alert.text.strip()
