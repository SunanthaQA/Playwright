import time

from playwright.sync_api import Error, Page

from pages.UploadInvoicePage import UploadInvoicePage
from tests.validationtexts import ValidationTexts
from utils import ExcelUtils


def test_add_invoice(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    try:
        invoice_page.login(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
                           ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2))
        invoice_page.upload_invoice(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1),
                                    ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 2),
                                    ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 3))
        invoice_page.verify_confirmation_message(ValidationTexts.SUCCESSFUL_INVOICE_UPLOAD)
    except (TimeoutError, Error, AssertionError) as e:
        print(f"Test 'add_invoice' failed: {e}")
        raise


def test_verify_created_invoice_status(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    try:
        invoice_page.login(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
                           ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2))
        invoice_page.search_invoice(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1))
        time.sleep(3)
        invoice_page.verify_invoice_in_list(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1))
    except (TimeoutError, Error, AssertionError) as e:
        print(f"Test 'verify_created_invoice_status' failed: {e}")
        raise


def test_verify_invoice_delete_status(setup_and_teardown) -> None:
    page = setup_and_teardown
    invoice_page = UploadInvoicePage(page)
    try:
        invoice_page.login(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 1),
                           ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Login", 2, 2))
        invoice_page.search_invoice(ExcelUtils.get_cell_data("ExcelFiles/Testdata.xlsx", "Invoice", 2, 1))
        time.sleep(3)
        invoice_page.delete_invoice()
        invoice_page.verify_deletion_message(ValidationTexts.SUCCESSFUL_INVOICE_DELETE)
    except (TimeoutError, Error, AssertionError) as e:
        print(f"Test 'verify_invoice_delete_status' failed: {e}")
        raise
