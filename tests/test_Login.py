import allure
import pytest
import time
from playwright.sync_api import Page, expect, Error

from pages.LoginPage import LoginPage
from tests.conftest import setup_and_teardown, attach_screenshot
from tests.validationtexts import ValidationTexts
from utils import ExcelUtils


#@allure.feature('Login Tests')
@allure.story('Login with valid credentials')
def test_login_with_valid_credentials(setup_and_teardown) -> None:
    page = setup_and_teardown
    login_p = LoginPage(page)
    credentials = {'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
                   'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2)}

    with allure.step('Perform login with valid credentials'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            login_p = login_p.do_login(credentials)
            expect(login_p.get_dashboard_check).to_be_visible()
            expect(login_p.get_dashboard_check).to_have_text(ValidationTexts.WELCOME_MESSAGE)
            attach_screenshot(page, "Valid Login Success")
        except (AssertionError, Error) as e:
            attach_screenshot(page, "Valid Login Failure")
            pytest.fail(f"Failed to login with valid credentials: {str(e)}")


@allure.story('Login with invalid email address')
def test_login_with_invalid_email_address(setup_and_teardown) -> None:
    page = setup_and_teardown
    login_p = LoginPage(page)
    credentials = {'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 3, 1),
                   'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 3, 2)}

    with allure.step('Perform login with invalid email address'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            login_p = login_p.do_login(credentials)
            actual_message = login_p.get_incorrect_email_message().strip()
            assert actual_message == ValidationTexts.LOGIN_FAILED
            attach_screenshot(page, "Invalid Email Login Success")
        except (AssertionError, Error) as e:
            attach_screenshot(page, "Invalid Email Login Failure")
            pytest.fail(f"Failed to handle invalid email address: {str(e)}")


@allure.story('Login with invalid password')
def test_login_with_invalid_password(setup_and_teardown) -> None:
    page = setup_and_teardown
    login_p = LoginPage(page)
    credentials = {'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 4, 1),
                   'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 4, 2)}

    with allure.step('Perform login with invalid password'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            login_p = login_p.do_login(credentials)
            actual_message = login_p.get_incorrect_email_message().strip()
            assert actual_message == ValidationTexts.LOGIN_FAILED
            attach_screenshot(page, "Invalid Password Login Success")
        except (AssertionError, Error) as e:
            attach_screenshot(page, "Invalid Password Login Failure")
            pytest.fail(f"Failed to handle invalid password: {str(e)}")


@allure.story('Required validation')
def test_required_validation(setup_and_teardown) -> None:
    page = setup_and_teardown
    login_p = LoginPage(page)
    with allure.step('Check required validation messages'):
        try:
            login_p.click_login_button()
            email_error_text, password_error_text = login_p.check_login_validation_message()
            assert (
                email_error_text == ValidationTexts.EMAIL_REQUIRED and
                password_error_text == ValidationTexts.PASSWORD_REQUIRED
            )
            attach_screenshot(page, "Required Validation Success")
        except (AssertionError, Error) as e:
            attach_screenshot(page, "Required Validation Failure")
            pytest.fail(f"Failed on required validation: {str(e)}")
