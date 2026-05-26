import re
import random
from datetime import datetime, timedelta

import allure
from playwright.sync_api import Page

from config import BASE_URL

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
}


class MainPage:
    URL = BASE_URL

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открыть главную страницу и принять куки")
    def open(self):
        self.page.goto(self.URL)
        self.page.get_by_role("button", name="Согласен", exact=True).click()

    @allure.step("Заполнить пункт отправления")
    def fill_from(self, city: str):
        self.page.get_by_role("textbox", name="Пункт отправления").click()
        self.page.get_by_role("textbox", name="Пункт отправления").fill(city)

    @allure.step("Заполнить пункт назначения")
    def fill_to(self, city: str):
        self.page.get_by_role("textbox", name="Выберите пункт назначения").click()
        self.page.get_by_role("textbox", name="Выберите пункт назначения").fill(city)

    @allure.step("Выбрать дату")
    def select_date(self, days_offset: int) -> datetime:
        target = datetime.now() + timedelta(days=days_offset)
        self.page.get_by_role("textbox", name="Выберите дату").click()
        self.page.get_by_role("button", name=re.compile(rf"{target.day} {MONTHS_RU[target.month]}")).click()
        return target

    def is_calendar_date_disabled(self, date: datetime) -> bool:
        self.page.get_by_role("textbox", name="Выберите дату").click()
        return self.page.locator(".react-calendar__month-view__days__day").filter(
            has_text=re.compile(rf"\b{date.day}\b")
        ).first.is_disabled()

    def get_city_suggestions(self, city: str) -> int:
        field = self.page.get_by_role("textbox", name="Пункт отправления")
        field.click()
        field.press_sequentially(city, delay=150)
        self.page.wait_for_timeout(1000)
        return self.page.locator('[class*="form-search__select"]').first.get_by_role("button").count()

    @allure.step("Нажать 'Найти билеты'")
    def submit(self):
        self.page.get_by_role("button", name="Найти билеты").click()

    @allure.step("Найти рейс {from_city} → {to_city}")
    def search(self, from_city: str, to_city: str, days_offset: int = None) -> datetime:
        if days_offset is None:
            days_offset = random.randint(3, 4)
        self.fill_from(from_city)
        self.fill_to(to_city)
        target = self.select_date(days_offset)
        self.submit()
        return target
