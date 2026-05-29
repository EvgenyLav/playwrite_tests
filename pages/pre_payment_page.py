import re

import allure
from playwright.sync_api import Page, expect


class PrePaymentPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Дождаться страницы подтверждения данных")
    def wait_for_page(self):
        expect(self.page.get_by_role("heading", name="Проверка данных")).to_be_visible(timeout=30000)

    @allure.step("Проверить наличие ФИО пассажира на странице подтверждения")
    def has_passenger_name(self, name: str) -> bool:
        return self.page.get_by_text(name).first.is_visible()

    @allure.step("Проверить наличие email на странице подтверждения")
    def has_email(self, email: str) -> bool:
        return self.page.get_by_text(email).first.is_visible()

    @allure.step("Получить итоговую стоимость на странице подтверждения")
    def get_total_price(self) -> str:
        # К оплате: and price are siblings — find innermost container holding both
        container = self.page.locator("*").filter(
            has_text=re.compile(r"К оплате")
        ).filter(
            has_text=re.compile(r"\d+\s*(?:EUR|BYN|USD|руб|₽)")
        ).last
        text = container.text_content()
        match = re.search(r"\d[\d\s.,]*(?:EUR|BYN|USD|руб|₽)", text)
        return match.group().strip() if match else text.strip()

    @allure.step("Проверить наличие текста на странице подтверждения")
    def has_text(self, text: str) -> bool:
        return self.page.get_by_text(text).first.is_visible()

    @allure.step("Нажать 'Оплатить'")
    def pay(self):
        self.page.get_by_role("button", name="Оплатить").click()
