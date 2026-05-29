import allure
from playwright.sync_api import Page


class SuccessPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Дождаться страницы успешной оплаты")
    def wait_for_page(self):
        self.page.get_by_role("heading", name="Оплата прошла успешно!").wait_for(timeout=15000)

    @allure.step("Скачать билет")
    def download_ticket(self):
        with self.page.expect_download() as download_info:
            self.page.get_by_role("button", name="Скачать билет(-ы)").click()
        return download_info.value
