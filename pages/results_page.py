import re
from datetime import datetime

import allure
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Дождаться загрузки результатов поиска")
    def wait_for_results(self):
        self.page.wait_for_selector("[class*='ListRatesItem']", timeout=30000)

    @allure.step("Получить заголовок маршрута со страницы результатов")
    def get_route_heading(self) -> str:
        return self.page.get_by_role("heading").filter(
            has_text=re.compile(r"[А-Яа-яЁё].+[А-Яа-яЁё]")
        ).first.text_content().strip()

    @allure.step("Получить даты из карточек рейсов")
    def get_displayed_dates(self) -> list[str]:
        return [
            el.text_content().strip()
            for el in self.page.locator("[class*='list-item__date']").all()
        ]

    @allure.step("Проверить наличие рейса {departure_time} перевозчика {carrier}")
    def trip_exists(self, departure_time: str, carrier: str) -> bool:
        locator = self.page.locator("[class*='ListRatesItem_list-item__']").filter(
            has_text=departure_time
        ).filter(
            has_text=carrier
        )
        try:
            locator.first.wait_for(timeout=15000)
            return True
        except PlaywrightTimeoutError:
            return False

    @allure.step("Получить цену рейса {departure_time} перевозчика {carrier}")
    def get_price(self, departure_time: str, carrier: str) -> str:
        card = self.page.locator("[class*='ListRatesItem_list-item__']").filter(
            has_text=departure_time
        ).filter(
            has_text=carrier
        ).first
        return card.locator("[class*='list-item-order__price']").text_content().strip()

    @allure.step("Выбрать рейс {departure_time} перевозчика {carrier}")
    def select_trip(self, departure_time: str, carrier: str):
        self.page.locator("[class*='ListRatesItem_list-item__']").filter(
            has_text=departure_time
        ).filter(
            has_text=carrier
        ).get_by_role("button", name="Выбрать билет").first.click()
