"""Tests for Main Dashboard interface after successful authentication."""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(scope="module")
def logged_in_dashboard():
    """Module-scoped fixture: logs in once and reuses session across dashboard tests."""
    base_url = os.getenv("APP_BASE_URL", "").strip()
    username = os.getenv("TEST_USERNAME", "").strip()
    password = os.getenv("TEST_PASSWORD", "").strip()
    if not base_url:
        pytest.skip("Set APP_BASE_URL in .env")
    if not username or not password:
        pytest.skip("TEST_USERNAME or TEST_PASSWORD not set in .env")

    options = Options()
    options.add_argument("--window-size=1365,900")
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.login(username, password)

    dashboard = DashboardPage(driver)
    dashboard.is_loaded()
    try:
        yield dashboard
    finally:
        driver.quit()


@pytest.mark.web
def test_dashboard_header_and_account(logged_in_dashboard):
    """Verify that dashboard displays university branding and correct logged-in account."""
    username = os.getenv("TEST_USERNAME", "")
    assert username in logged_in_dashboard.get_displayed_username(), f"Account {username} not found in header"
    assert "Kiến trúc Hà Nội" in logged_in_dashboard.driver.page_source


@pytest.mark.web
def test_filter_tabs_presence(logged_in_dashboard):
    """Verify all expected functional filter tabs exist and can be activated."""
    expected_tabs = ["Tất cả", "Quản lý đào tạo", "Hành chính", "Khảo thí", "KPI"]
    for tab in expected_tabs:
        logged_in_dashboard.select_filter_tab(tab)
        time.sleep(0.3)
        assert logged_in_dashboard.get_active_tab_name() == tab
    # Reset back to Tất cả
    logged_in_dashboard.select_filter_tab("Tất cả")


@pytest.mark.web
def test_search_filters_modules(logged_in_dashboard):
    """Verify search input dynamically filters the module cards."""
    logged_in_dashboard.select_filter_tab("Tất cả")
    logged_in_dashboard.search_module("nhân sự")
    time.sleep(0.5)

    cards = logged_in_dashboard.get_app_cards()
    visible_cards = [c for c in cards if c["visible"] and c["name"]]
    assert any("nhân sự" in c["name"].lower() for c in visible_cards), (
        "Expected 'Quản lý nhân sự' module card to be visible in search results"
    )
    # Clear search
    logged_in_dashboard.search_module("")
    logged_in_dashboard.select_filter_tab("Tất cả")


@pytest.mark.web
def test_quan_ly_nhan_su_module_is_listed(logged_in_dashboard):
    """Verify that 'Quản lý nhân sự' exists in module catalog."""
    logged_in_dashboard.select_filter_tab("Tất cả")
    cards = logged_in_dashboard.get_app_cards()
    ns_card = next((c for c in cards if "nhân sự" in c["name"].lower()), None)
    assert ns_card is not None, "'Quản lý nhân sự' module not found in catalog"


@pytest.mark.web
def test_quan_ly_nhan_su_module_permission_status(logged_in_dashboard):
    """Verify that 'Quản lý nhân sự' module is currently disabled for this account."""
    logged_in_dashboard.select_filter_tab("Tất cả")
    cards = logged_in_dashboard.get_app_cards()
    ns_card = next((c for c in cards if "nhân sự" in c["name"].lower()), None)
    assert ns_card is not None
    assert ns_card["disabled"] is True, "Quản lý nhân sự was expected to be disabled for this account"
