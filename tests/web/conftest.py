"""Shared fixtures for web UI tests."""

import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()


@pytest.fixture
def browser():
    base_url = os.getenv("APP_BASE_URL", "").strip()
    if not base_url:
        pytest.skip("Set APP_BASE_URL to the authorized test environment in .env")

    options = Options()
    if os.getenv("HEADLESS", "false").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    browser_name = os.getenv("BROWSER", "chrome").strip().lower()
    if browser_name != "chrome":
        pytest.skip(f"Browser '{browser_name}' is not configured in this starter scaffold")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1365, 900)
    driver.get(base_url)
    try:
        yield driver
    finally:
        driver.quit()
