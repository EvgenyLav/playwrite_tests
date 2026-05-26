import re

import allure
from playwright.sync_api import Page


class PaymentPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Ввести данные карты")
    def fill_card(self, card_number: str, expiry: str, cvv: str):
        self.page.wait_for_url(re.compile(r"abby\.rbsuat\.com"), timeout=30000)
        self.page.get_by_role("textbox", name="0000 0000 0000").fill(card_number)
        self.page.get_by_role("textbox", name="/00").fill(expiry)
        self.page.get_by_role("textbox", name="000", exact=True).fill(cvv)
        self.page.locator("[data-test-id='submitPayByCardForm']").click()

    @allure.step("Пройти 3DS-подтверждение")
    def submit_3ds(self, password: str):
        self.page.get_by_role("textbox", name="Пароль").press_sequentially(password, delay=300)
        self.page.wait_for_url(re.compile(r"intercars-tickets\.com"), timeout=30000)
