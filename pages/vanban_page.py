"""Page Object for Van Ban Management Portal (vanban.hau.edu.vn).
Phụ trách: Nguyễn Quang Huy.
Phạm vi: Cổng Quản lý văn bản điều hành, thanh menu bên trái, các ô tra cứu nhanh và widget dashboard.
"""

from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class VanBanPage(BasePage):
    URL = "https://vanban.hau.edu.vn"

    # Selectors
    PAGE_TITLE_CONTAINER = (By.CSS_SELECTOR, "body, header, .content-header")
    SIDEBAR_MENU = (By.CSS_SELECTOR, "ul.sidebar-menu, .sidebar, nav")
    SIDEBAR_LINKS = (By.CSS_SELECTOR, "ul.sidebar-menu li a, .nav-item a, .sidebar a")

    # Fast search fields
    SEARCH_INPUTS = (By.CSS_SELECTOR, "input[placeholder*='Tra cứu'], input[placeholder*='Tìm']")
    DATE_FROM = (By.ID, "txtTuNgay")
    DATE_TO = (By.ID, "txtDenNgay")
    DEPT_SEARCH = (By.ID, "homeJstreeSearch")
    USER_SEARCH = (By.ID, "homeJstreeUserSearch")
    TASK_SEARCH = (By.ID, "tkpbDsTim")

    # Widgets and statistic panels
    WIDGET_PANELS = (By.CSS_SELECTOR, ".box, .widget, .card, .panel, .dashboard-stat")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)

    def navigate_to(self) -> None:
        """Chuyển hướng đến cổng quản lý văn bản."""
        self.driver.get(self.URL)

    def is_loaded(self) -> bool:
        """Đợi trang quản lý văn bản tải xong tiêu đề và cấu trúc."""
        self.wait.until(EC.url_contains("vanban.hau.edu.vn"))
        self.wait.until(lambda d: "văn bản" in d.title.lower() or "quản lý" in d.title.lower())
        return True

    def get_sidebar_menu_titles(self) -> List[str]:
        """Lấy danh sách các nhãn menu ở thanh bên trái."""
        elements = self.driver.find_elements(*self.SIDEBAR_LINKS)
        results = []
        for elem in elements:
            text = (elem.text or elem.get_attribute("textContent") or "").strip()
            if text and text not in results:
                results.append(text)
        return results

    def get_quick_search_placeholders(self) -> List[str]:
        """Lấy danh sách placeholder của các ô tra cứu nhanh."""
        inputs = self.driver.find_elements(*self.SEARCH_INPUTS)
        return [inp.get_attribute("placeholder") for inp in inputs if inp.get_attribute("placeholder")]

    def has_date_filter_fields(self) -> bool:
        """Kiểm tra sự hiện diện của bộ lọc Từ ngày - Đến ngày."""
        from_elem = self.driver.find_elements(*self.DATE_FROM)
        to_elem = self.driver.find_elements(*self.DATE_TO)
        return len(from_elem) > 0 and len(to_elem) > 0

    def get_widget_count(self) -> int:
        """Đếm số khối widget / panel thống kê trên giao diện."""
        return len(self.driver.find_elements(*self.WIDGET_PANELS))

