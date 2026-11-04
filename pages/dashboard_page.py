"""Page Object for Main Dashboard page after login."""

from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class DashboardPage(BasePage):
    USER_CODE = (By.ID, "usercode")
    USER_AVATAR = (By.ID, "userAvatar")
    USER_MENU_TOGGLE = (By.ID, "userInfoToggle")
    DROPDOWN_MENU = (By.ID, "dropdownMenu")
    CHANGE_PASSWORD_BTN = (By.ID, "changepass-btn")
    LOGOUT_BTN = (By.ID, "logout-btn")

    SEARCH_INPUT = (By.ID, "searchInput")
    SEARCH_BUTTON = (By.ID, "searchBtn")

    FILTER_TABS = (By.CSS_SELECTOR, ".filter-tab")
    ACTIVE_TAB = (By.CSS_SELECTOR, ".filter-tab.active")
    APP_CARDS = (By.CSS_SELECTOR, "a.app-card")
    RESULT_BADGE = (By.XPATH, "//*[contains(text(), 'kết quả')]")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    def is_loaded(self) -> bool:
        """Wait until redirected to main dashboard and user info is loaded."""
        redirected = self.wait.until(EC.url_contains("main.hau.edu.vn"))
        self.wait.until(
            lambda d: len(
                (d.find_element(*self.USER_CODE).text or d.find_element(*self.USER_CODE).get_attribute("textContent") or "").strip()
            ) > 2
        )
        return redirected

    def get_displayed_username(self) -> str:
        """Get the username/account string displayed in header."""
        elem = self.wait.until(lambda d: d.find_element(*self.USER_CODE))
        return (elem.text or elem.get_attribute("textContent") or "").strip()

    def search_module(self, keyword: str) -> None:
        """Type keyword into search input and trigger search."""
        inp = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        inp.clear()
        inp.send_keys(keyword)
        search_btn = self.driver.find_element(*self.SEARCH_BUTTON)
        self.driver.execute_script("arguments[0].click();", search_btn)

    def select_filter_tab(self, tab_name: str) -> None:
        """Click on a specific filter tab."""
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//button[contains(@class, 'filter-tab') and contains(text(), '{tab_name}')]"))
        )
        self.driver.execute_script("arguments[0].click();", tab)

    def get_active_tab_name(self) -> str:
        tab = self.driver.find_element(*self.ACTIVE_TAB)
        return tab.text.strip()

    def get_badge_text(self) -> str:
        badges = self.driver.find_elements(*self.RESULT_BADGE)
        return badges[0].text.strip() if badges else ""

    def get_app_cards(self) -> List[Dict[str, any]]:
        """Return list of app card details."""
        cards = self.driver.find_elements(*self.APP_CARDS)
        results = []
        for c in cards:
            name_elems = c.find_elements(By.CSS_SELECTOR, ".app-card-name")
            name = name_elems[0].get_attribute("textContent").strip() if name_elems else c.get_attribute("textContent").strip()
            classes = c.get_attribute("class") or ""
            href = c.get_attribute("href") or ""
            is_disabled = "app-disabled" in classes
            results.append({
                "name": name,
                "disabled": is_disabled,
                "href": href,
                "visible": c.is_displayed()
            })
        return results

    def open_user_dropdown(self) -> None:
        dropdown_btn = self.wait.until(EC.element_to_be_clickable(self.USER_MENU_TOGGLE))
        dropdown_btn.click()
