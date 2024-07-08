import base64
from pathlib import Path

from playwright.sync_api import Page, Error


class BasePage:
    elements = {}

    def __init__(self, page: Page):
        self.page = page

    def get_element(self, name):
        element_type, value = self.elements.get(name)

        if element_type == "label":
            return self.page.get_by_label(value)
        elif element_type == "locator":
            return self.page.locator(value)
        elif element_type == "role":
            return self.page.get_by_role(value)
        else:
            raise ValueError(f"Unsupported element type: {element_type}")

    def login(self, username: str, password: str):
        try:
            self.get_element('email_field').fill(username)
            self.get_element('password_field').fill(password)
            self.get_element('login_button').click()
            # self.get_element('ignore_popup_button').get_by_role("button").click()
        except (TimeoutError, Error) as e:
            print(f"Login failed: {e}")
        raise
