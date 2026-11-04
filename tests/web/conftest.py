"""Shared fixtures for web UI tests.

Bổ sung Tuần 3 (Nguyễn Quang Huy):
  - Hook tự động chụp ảnh khi test thất bại (auto-screenshot on failure).
  - Fixture logged_in_driver dùng chung cho các bộ test cần đăng nhập sẵn.
"""

import os
import datetime
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage

load_dotenv()


def _make_driver() -> webdriver.Chrome:
    """Khởi tạo Chrome với cấu hình từ .env."""
    base_url = os.getenv("APP_BASE_URL", "").strip()
    if not base_url:
        pytest.skip("Set APP_BASE_URL to the authorized test environment in .env")

    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--window-size=1365,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    browser_name = os.getenv("BROWSER", "chrome").strip().lower()
    if browser_name != "chrome":
        pytest.skip(f"Browser '{browser_name}' is not configured in this starter scaffold")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.get(base_url)
    return driver


@pytest.fixture
def browser():
    """Driver đơn giản trỏ tới APP_BASE_URL (không đăng nhập sẵn)."""
    driver = _make_driver()
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture(scope="module")
def logged_in_driver():
    """Module-scoped fixture: đăng nhập một lần, dùng chung cho cả module test."""
    username = os.getenv("TEST_USERNAME", "").strip()
    password = os.getenv("TEST_PASSWORD", "").strip()
    if not username or not password:
        pytest.skip("TEST_USERNAME hoặc TEST_PASSWORD chưa được cấu hình trong .env")

    driver = _make_driver()
    login_page = LoginPage(driver)
    login_page.login(username, password)
    try:
        yield driver
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# Hook: tự động chụp ảnh màn hình khi test FAIL – Tuần 3
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Chụp ảnh màn hình và lưu vào evidence/web/ khi test FAIL."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        # Lấy driver từ fixture nếu có
        for fixture_name in ("driver", "browser", "logged_in_driver", "logged_in_dashboard"):
            driver = item.funcargs.get(fixture_name)
            if driver is not None:
                # logged_in_dashboard là DashboardPage, không phải driver
                if hasattr(driver, "driver"):
                    driver = driver.driver
                break

        if driver is not None:
            os.makedirs("evidence/web", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
            filename = f"evidence/web/FAIL_{safe_name}_{timestamp}.png"
            try:
                driver.save_screenshot(filename)
            except Exception:
                pass  # Không để lỗi chụp ảnh làm hỏng report
