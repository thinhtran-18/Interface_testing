"""Cổng Quản lý văn bản điều hành (Van Ban Management Test Suite).
Phụ trách chính: Nguyễn Quang Huy.
Phạm vi: Kiểm thử giao diện trang vanban.hau.edu.vn, hệ thống menu điều hướng trái,
các ô tra cứu nhanh, bộ lọc thời gian và các khối widget thống kê theo khảo sát thực tế.
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.vanban_page import VanBanPage


@pytest.fixture(scope="module")
def vanban_page():
    """Module-scoped fixture: Đăng nhập Cổng chính, chuyển tiếp sang Cổng Văn bản."""
    base_url = os.getenv("APP_BASE_URL", "").strip()
    username = os.getenv("TEST_USERNAME", "").strip()
    password = os.getenv("TEST_PASSWORD", "").strip()
    if not base_url:
        pytest.skip("Chưa cấu hình APP_BASE_URL trong .env")
    if not username or not password:
        pytest.skip("Chưa cấu hình TEST_USERNAME hoặc TEST_PASSWORD trong .env")

    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--window-size=1365,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)

    try:
        # Bước 1: Đăng nhập SSO qua Cổng chính
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(username, password)

        # Bước 2: Chờ dashboard cổng chính sẵn sàng
        dash = DashboardPage(driver)
        dash.is_loaded()

        # Bước 3: Điều hướng sang cổng Quản lý văn bản
        vb_page = VanBanPage(driver)
        vb_page.navigate_to()
        vb_page.is_loaded()

        yield vb_page
    finally:
        driver.quit()


@pytest.mark.web
def test_WEB_VANBAN_01_navigation_and_title(vanban_page):
    """WEB-VB-01: Xác thực điều hướng thành công vào Cổng Văn bản và tiêu đề trang."""
    assert vanban_page.is_loaded(), "Không thể tải trang Quản lý văn bản"
    assert "vanban.hau.edu.vn" in vanban_page.driver.current_url
    assert "quản lý văn bản" in vanban_page.driver.title.lower()


@pytest.mark.web
def test_WEB_VANBAN_02_sidebar_menu_structure(vanban_page):
    """WEB-VB-02: Kiểm tra sự hiện diện của các nhóm menu cốt lõi trên thanh bên trái."""
    menu_titles = vanban_page.get_sidebar_menu_titles()
    full_text = " ".join(menu_titles).lower()

    # Khảo sát Tuần 1: Trình ký, Văn bản đi, Văn bản đến, Lịch, Quản lý công việc
    expected_groups = ["trình ký", "văn bản đi", "văn bản đến", "lịch", "công việc"]
    for grp in expected_groups:
        assert grp in full_text, f"Thiếu phân hệ menu cốt lõi: '{grp}'"


@pytest.mark.web
def test_WEB_VANBAN_03_quick_search_inputs(vanban_page):
    """WEB-VB-03: Kiểm tra sự hiện diện của các ô tra cứu nhanh theo nghiệp vụ."""
    placeholders = vanban_page.get_quick_search_placeholders()
    assert len(placeholders) >= 2, f"Cần ít nhất 2 ô tra cứu nhanh, tìm thấy {len(placeholders)}"
    assert any("tra cứu" in p.lower() for p in placeholders), "Không tìm thấy ô tra cứu nhanh 'Tra cứu...'"


@pytest.mark.web
def test_WEB_VANBAN_04_date_filter_fields(vanban_page):
    """WEB-VB-04: Kiểm tra sự tồn tại của bộ lọc khoảng thời gian (Từ ngày - Đến ngày)."""
    assert vanban_page.has_date_filter_fields(), "Không tìm thấy bộ lọc ngày (txtTuNgay / txtDenNgay)"


@pytest.mark.web
def test_WEB_VANBAN_05_dashboard_widgets_presence(vanban_page):
    """WEB-VB-05: Kiểm tra các khối Widget/Thống kê tổng quan trên Dashboard Quản lý văn bản."""
    count = vanban_page.get_widget_count()
    assert count >= 4, f"Số lượng khối widget thống kê không đủ theo thiết kế (mong đợi >= 4, thực tế {count})"

    os.makedirs("evidence/web", exist_ok=True)
    vanban_page.driver.save_screenshot("evidence/web/vanban_dashboard_widgets.png")

