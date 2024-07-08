import base64
import logging
from pathlib import Path
from venv import logger

import allure
import pytest
from playwright.sync_api import sync_playwright
from utils import ReadConfigurations
from slugify import slugify


@pytest.fixture(scope="function")
def setup_and_teardown():
    with sync_playwright() as p:
        browser_type = ReadConfigurations.read_configuration("basic info", "browser")
        if browser_type == "chrome":
            browser = p.chromium.launch(headless=False)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=False)
        else:
            raise ValueError("Provide a valid browser name from this list: chrome or firefox")

        context = browser.new_context()
        page = context.new_page()
        app_url = ReadConfigurations.read_configuration("basic info", "url")
        viewport_width = 1920
        viewport_height = 1080
        page.set_viewport_size({"width": viewport_width, "height": viewport_height})
        page.goto(app_url)
        yield page
        browser.close()


def attach_screenshot(page, name="Screenshot"):
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
