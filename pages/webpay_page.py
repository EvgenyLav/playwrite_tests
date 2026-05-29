import re

import allure
from playwright.sync_api import Page


class WebPayPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Ввести данные карты WebPay")
    def fill_card(self, card):
        self.page.wait_for_url(re.compile(r"securesandbox\.webpay\.by"), timeout=30000)
        self.page.get_by_role("textbox", name="месяц").fill(card.month)
        self.page.get_by_role("textbox", name="год").fill(card.year)
        self.page.get_by_role("textbox", name="Имя держателя").fill(card.holder)
        self.page.get_by_role("textbox", name="CVV").fill(card.cvv)
        self.page.get_by_role("textbox", name="email email").fill(card.email)
        self.page.get_by_role("button", name=re.compile(r"ОПЛАТИТЬ")).click()
        self.page.wait_for_url(re.compile(r"intercars-tickets\.com"), timeout=30000)

    @allure.step("Оплатить через WebPay")
    def complete(self, card):
        self.fill_card(card)
