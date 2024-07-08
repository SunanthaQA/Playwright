import time

from playwright.sync_api import Page, expect, Error

from BasePage.basepage import BasePage


class UploadInvoicePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    elements = {
        'email_field': ("label", "Email Address *"),
        'password_field': ("label", "Password *"),
        'login_button': ("label", "LOG IN"),
        'ignore_popup_button': ("role", "heading:Test Badge:exact"),
        'my_indigo_icon_dashborad': ('label', 'My Indigo (FRS)'),
        'invoice_icon': ("locator", "#homepage_icon_210"),
        'nav_invoices': ("locator", "#navLeft_Invoices"),
        'upload_invoice_icon': ("locator",
                                "//mat-icon[@class='mat-icon notranslate material-icons-outlined material-icons "
                                "mat-ligature-font mat-icon-no-color']"),
        'search_field': (
            "locator",
            "//input[@placeholder='Search Organisation, registration number, invoice number or amount']"),
        'invoice_number_field': ("label", "Invoice Number *"),
        'total_amount_field': ("label", "Total Amount *"),
        'client_dropdown': ("label", "Client *"),
        'client_option': ("locator", "//span[contains(text(), 'Indigo Client')]"),
        'upload_input': ("locator", "//input[@class='ng-star-inserted']"),
        'cookie_message_dismiss': ("label", "dismiss cookie message"),
        'add_new_button': ("label", "Add New"),
        'confirmation_message': ("locator", "//span[@class='alert-message']"),
        'delete_icon': ("locator",
                        "//mat-icon[@class='mat-icon notranslate rebrand-icon gray material-icons-outlined "
                        "material-icons mat-ligature-font mat-icon-no-color' and text()=' delete']"),
        'delete_button': ("locator", "//span[normalize-space()='Delete']"),
        'delete_ok': ("locator", "//span[@class='mat-button-wrapper' and text() ='OK']")
    }

    def get_sample_element(self, name):
        locator_type, value = self.elements[name]
        if locator_type == "label":
            return self.page.get_by_label(value)
        elif locator_type == "locator":
            return self.page.locator(value)
        elif locator_type == "role":
            return self.page.get_by_role(value)

    def login(self, username: str, password: str):
        try:
            self.get_element('email_field').fill(username)
            self.get_element('password_field').fill(password)
            self.get_element('login_button').click()
            # self.get_element('ignore_popup_button').get_by_role("button").click()
            return UploadInvoicePage(self.page)
        except (TimeoutError, Error) as e:
            print(f"Login failed: {e}")
        raise

    def upload_invoice(self, invoice_number: str, total_amount: str, file_path: str) -> None:
        try:
            self.get_element('invoice_icon').click()
            self.get_element('nav_invoices').click()
            self.get_element('upload_invoice_icon').click()
            self.get_element('invoice_number_field').fill(invoice_number)
            self.get_element('total_amount_field').fill(total_amount)
            self.get_element('client_dropdown').click()
            self.get_element('client_option').click()
            self.page.keyboard.press('Tab')
            time.sleep(3)
            self.page.keyboard.press('Enter')
            self.page.keyboard.press('Enter')
            self.get_element('upload_input').set_input_files(file_path)
            self.get_element('cookie_message_dismiss').click()
            self.get_element('add_new_button').click()
            self.get_element('delete_ok').click()
        except (TimeoutError, Error) as e:
            print(f"Invoice upload failed: {e}")
            raise

    def verify_confirmation_message(self, expected_message: str) -> None:
        try:
            expect(self.get_element('confirmation_message')).to_have_text(expected_message)
        except AssertionError as e:
            print(f"Confirmation message verification failed: {e}")
            raise

    def search_invoice(self, keyword: str) -> None:
        try:
            self.get_element('invoice_icon').get_by_role("img").click()
            self.get_element('nav_invoices').click()
            self.get_element('search_field').fill(keyword)
            time.sleep(3)
            self.page.keyboard.press('Enter')
        except (TimeoutError, Error) as e:
            print(f"Invoice search failed: {e}")
            raise

    def verify_invoice_in_list(self, keyword: str) -> None:
        try:
            element = self.page.locator(
                f"//div[contains(@class, 'text-truncate-w100') and contains(text(), '{keyword}')]")
            expect(element).to_be_visible()
            assert element.inner_text() == keyword
        except AssertionError as e:
            print(f"Invoice verification in list failed: {e}")
            raise

    def delete_invoice(self) -> None:
        try:
            self.get_element('delete_icon').click()
            self.get_element('delete_button').click()
        except (TimeoutError, Error) as e:
            print(f"Invoice deletion failed: {e}")
            raise

    def verify_deletion_message(self, expected_message: str) -> None:
        try:
            actual_message = self.get_element('confirmation_message').inner_text()
            assert actual_message.strip() == expected_message.strip()
        except AssertionError as e:
            print(f"Deletion message verification failed: {e}")
            raise
