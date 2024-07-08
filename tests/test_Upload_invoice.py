import time

import allure
import pytest
from playwright.sync_api import Error, Page

from pages.UploadInvoicePage import UploadInvoicePage
from tests.conftest import attach_screenshot
from tests.validationtexts import ValidationTexts
from utils import ExcelUtils


#@allure.feature('Invoice Tests')
@allure.story('Add Invoice')
def test_add_invoice(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    credentials = {
        'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
        'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2)
    }
    invoice_data = {
        'invoice_number': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1),
        'invoice_amount': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 2),
        'attachment': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 3)
    }

    with allure.step('Login and upload invoice'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Invoice Number: {invoice_data['invoice_number']}", name="Invoice Number",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Invoice Amount: {invoice_data['invoice_amount']}", name="Invoice Amount",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Attachment: {invoice_data['attachment']}", name="Attachment",
                      attachment_type=allure.attachment_type.TEXT)
    try:
        invoice_page.login(credentials['username'], credentials['password'])
        invoice_page.upload_invoice(invoice_data['invoice_number'], invoice_data['invoice_amount'],
                                    invoice_data['attachment'])
        invoice_page.verify_confirmation_message(ValidationTexts.SUCCESSFUL_INVOICE_UPLOAD)
        attach_screenshot(page, "Invoice Upload Success")
    except (TimeoutError, Error, AssertionError) as e:
        attach_screenshot(page, "Invoice Upload Failure")
        print(f"Test 'add_invoice' failed: {e}")
        pytest.fail(f"Failed to add invoice: {str(e)}")


@allure.story('Search created Invoice')
def test_verify_created_invoice_status(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    credentials = {
        'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
        'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2)
    }
    invoice_number = ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1)

    with allure.step('Login and verify created invoice status'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Invoice Number: {invoice_number}", name="Invoice Number",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            invoice_page.login(credentials['username'], credentials['password'])
            invoice_page.search_invoice(invoice_number)
            time.sleep(3)
            invoice_page.verify_invoice_in_list(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1))
            attach_screenshot(page, "Invoice Verification Success")
        except (TimeoutError, Error, AssertionError) as e:
            attach_screenshot(page, "Invoice Verification Failure")
            print(f"Test 'verify_created_invoice_status' failed: {e}")
            pytest.fail(f"Failed to verify created invoice status: {str(e)}")


@allure.story('Delete created Invoice')
def test_verify_invoice_delete_status(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    credentials = {
        'username': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
        'password': ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2)
    }
    invoice_number = ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1)

    with allure.step('Login and delete invoice'):
        allure.attach(f"Username: {credentials['username']}", name="Input Username",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Password: {credentials['password']}", name="Input Password",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"Invoice Number: {invoice_number}", name="Invoice Number",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            invoice_page.login(credentials['username'], credentials['password'])
            invoice_page.search_invoice(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1))
            time.sleep(3)
            invoice_page.delete_invoice()
            invoice_page.verify_deletion_message(ValidationTexts.SUCCESSFUL_INVOICE_DELETE)
            attach_screenshot(page, "Invoice Deletion Success")
        except (TimeoutError, Error, AssertionError) as e:
            attach_screenshot(page, "Invoice Deletion Failure")
            print(f"Test 'verify_invoice_delete_status' failed: {e}")
            pytest.fail(f"Failed to verify invoice delete status: {str(e)}")
