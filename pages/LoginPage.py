# LoginPage.py
from playwright.sync_api import Page, Locator

from BasePage.basepage import BasePage
from pages.UploadInvoicePage import UploadInvoicePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # XPaths
    elements = {
            'email_field': ("label", "Email Address *"),
            'password_field': ("label", "Password *"),
            'remember_me_checkbox': ("locator", ".mat-checkbox-inner-container"),
            'login_button': ("locator", "//button[@class='mat-focus-indicator primary mat-raised-button mat-button-base']"),
            'ignore_popup_button': ("locator", "role=heading[name='Test Badge'] >> role=button"),
            'dashboard_check': ("locator", "//div[@class='welcome-message theme-text']"),
            'incorrect_email_message': ("locator", "//mat-error[@class='mat-error error ng-star-inserted']"),
            'email_required_message': ("locator","//div/mat-error[@class='mat-error ng-tns-c113-1 ng-star-inserted']"),
            'password_required_message': ("locator", "//div/mat-error[@class='mat-error ng-tns-c113-2 ng-star-inserted']"),
        }

    def enter_username(self, username: str) -> None:
        username_field = self.get_element('email_field')
        username_field.clear()
        username_field.fill(username)

    def enter_password(self, password: str) -> None:
        password_field = self.get_element('password_field')
        password_field.clear()
        password_field.fill(password)

    def check_remember_me(self) -> None:
        remember_me_checkbox = self.get_element('remember_me_checkbox')
        remember_me_checkbox.click()

    def click_login_button(self) -> None:
        login_button = self.get_element('login_button')
        login_button.click()

    def click_and_ignore_popup(self) -> None:
        ignore_popup_button = self.get_element('ignore_popup_button')
        ignore_popup_button.click()

    def do_login(self, credentials: dict):
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.check_remember_me()
        self.click_login_button()
        # self.click_and_ignore_popup()
        return LoginPage(self.page)

    @property
    def get_dashboard_check(self) -> Locator:
        return self.get_element('dashboard_check')

    def get_incorrect_email_message(self) -> str:
        error_message = self.get_element('incorrect_email_message')
        return error_message.text_content()

    def get_email_required_message(self) -> str:
        email_required = self.get_element('email_required_message')
        return email_required.text_content()

    def get_password_required_message(self) -> str:
        password_required = self.get_element('password_required_message')
        return password_required.text_content()

    def check_login_validation_message(self) -> tuple:
        email_text = self.get_email_required_message()
        password_text = self.get_password_required_message()
        return email_text, password_text
