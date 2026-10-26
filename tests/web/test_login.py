"""Biểu mẫu & Xác thực (Form & Authentication Test Suite).
Phụ trách chính: Nguyễn Quang Huy.
Phạm vi: Kiểm thử giao diện biểu mẫu đăng nhập, kiểm tra dữ liệu đầu vào hợp lệ/không hợp lệ/biên và các thông báo lỗi.
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(scope="module")
def driver():
    """Module-scoped driver: runs all login form tests in a single clean browser session."""
    base_url = os.getenv("APP_BASE_URL", "").strip()
    if not base_url:
        pytest.skip("Chưa cấu hình APP_BASE_URL trong .env")

    options = Options()
    options.add_argument("--window-size=1365,900")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    drv = webdriver.Chrome(options=options)
    drv.get(base_url)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture(scope="module")
def login_page(driver):
    """Module-scoped login page object."""
    page = LoginPage(driver)
    page.is_loaded()
    return page


@pytest.mark.web
def test_WEB_FORM_01_elements_display_and_attributes(login_page, driver):
    """WEB-FORM-01: Kiểm tra sự tồn tại và thuộc tính của các phần tử trên biểu mẫu đăng nhập."""
    assert login_page.is_loaded(), "Biểu mẫu đăng nhập chưa được tải"
    assert "KIẾN TRÚC" in driver.title.upper(), f"Tiêu đề trang không đúng: {driver.title}"

    user_input = driver.find_element(*login_page.USERNAME_INPUT)
    assert user_input.is_displayed(), "Ô nhập tài khoản không hiển thị"
    assert "tên đăng nhập" in user_input.get_attribute("placeholder").lower()

    pass_input = driver.find_element(*login_page.PASSWORD_INPUT)
    assert pass_input.is_displayed(), "Ô nhập mật khẩu không hiển thị"
    assert pass_input.get_attribute("type") == "password"

    btn = driver.find_element(*login_page.LOGIN_BUTTON)
    assert btn.is_displayed(), "Nút Đăng nhập không hiển thị"
    assert "đăng nhập" in btn.text.lower()


@pytest.mark.web
def test_WEB_FORM_02_password_visibility_toggle(login_page):
    """WEB-FORM-02: Kiểm tra tương tác nút con mắt (Eye Toggle) để hiển thị/ẩn mật khẩu."""
    assert login_page.get_password_input_type() == "password"

    login_page.toggle_password_visibility()
    time.sleep(0.3)
    assert login_page.get_password_input_type() == "text", "Mật khẩu chưa chuyển sang dạng hiển thị"

    login_page.toggle_password_visibility()
    time.sleep(0.3)
    assert login_page.get_password_input_type() == "password", "Mật khẩu chưa chuyển về dạng ẩn"


@pytest.mark.web
def test_WEB_FORM_03_remember_login_checkbox_toggle(login_page):
    """WEB-FORM-03: Kiểm tra tương tác checkbox 'Nhớ thông tin đăng nhập'."""
    initial_state = login_page.is_remember_checked()

    login_page.toggle_remember()
    time.sleep(0.2)
    assert login_page.is_remember_checked() != initial_state

    login_page.toggle_remember()
    time.sleep(0.2)
    assert login_page.is_remember_checked() == initial_state


@pytest.mark.web
def test_WEB_FORM_04_empty_credentials_validation(login_page, driver):
    """WEB-FORM-04: Kiểm tra cảnh báo lỗi khi gửi biểu mẫu rỗng (để trống cả user và pass)."""
    login_page.enter_username("")
    login_page.enter_password("")
    login_page.click_login()
    time.sleep(1)

    error_msg = login_page.get_error_message()
    assert "Vui lòng nhập tên đăng nhập" in error_msg
    assert "Vui lòng nhập mật khẩu" in error_msg

    os.makedirs("evidence/web", exist_ok=True)
    driver.save_screenshot("evidence/web/WEB_FORM_04_empty_credentials.png")


@pytest.mark.web
def test_WEB_FORM_05_empty_password_validation(login_page):
    """WEB-FORM-05: Kiểm tra cảnh báo lỗi khi chỉ nhập tài khoản mà bỏ trống mật khẩu."""
    login_page.enter_username("035187013852")
    login_page.enter_password("")
    login_page.click_login()
    time.sleep(1)

    error_msg = login_page.get_error_message()
    assert "Vui lòng nhập mật khẩu" in error_msg
    assert "Vui lòng nhập tên đăng nhập" not in error_msg


@pytest.mark.web
def test_WEB_FORM_06_empty_username_validation(login_page):
    """WEB-FORM-06: Kiểm tra cảnh báo lỗi khi chỉ nhập mật khẩu mà bỏ trống tài khoản."""
    login_page.enter_username("")
    login_page.enter_password("123@123")
    login_page.click_login()
    time.sleep(1)

    error_msg = login_page.get_error_message()
    assert "Vui lòng nhập tên đăng nhập" in error_msg
    assert "Vui lòng nhập mật khẩu" not in error_msg


@pytest.mark.web
def test_WEB_FORM_07_invalid_credentials_error_message(login_page, driver):
    """WEB-FORM-07: Kiểm tra thông báo lỗi khi nhập tài khoản hoặc mật khẩu không chính xác."""
    login_page.enter_username("tai_khoan_gia_dinh_9999")
    login_page.enter_password("mat_khau_sai_123")
    login_page.click_login()
    time.sleep(1.5)

    error_msg = login_page.get_error_message()
    assert "Tên đăng nhập hoặc mật khẩu không đúng" in error_msg
    driver.save_screenshot("evidence/web/WEB_FORM_07_invalid_credentials.png")


@pytest.mark.web
def test_WEB_FORM_08_successful_login_with_valid_credentials(login_page, driver):
    """WEB-FORM-08: Kiểm tra đăng nhập thành công với tài khoản hợp lệ và chuyển hướng về cổng chính."""
    username = os.getenv("TEST_USERNAME", "").strip()
    password = os.getenv("TEST_PASSWORD", "").strip()
    if not username or not password:
        pytest.skip("Chưa cấu hình TEST_USERNAME hoặc TEST_PASSWORD trong .env")

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded(), "Hệ thống không chuyển hướng vào Cổng quản trị sau khi đăng nhập đúng"
    assert "main.hau.edu.vn" in driver.current_url
    assert username in dashboard.get_displayed_username()
