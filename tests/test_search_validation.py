from datetime import datetime, timedelta

import allure
from playwright.sync_api import expect

from pages.main_page import MainPage


@allure.epic("Бронирование билетов")
@allure.feature("Валидация формы поиска")
@allure.severity(allure.severity_level.NORMAL)
class TestSearchValidation:

    @allure.story("Обязательные поля")
    @allure.title("Сабмит пустой формы — поиск не выполняется")
    def test_empty_form_does_not_submit(self, page):
        main = MainPage(page)
        main.open()
        main.submit()

        expect(page).to_have_url(MainPage.URL, timeout=3000)

    @allure.story("Обязательные поля")
    @allure.title("Поиск без даты — поиск не выполняется")
    def test_missing_date_does_not_submit(self, page):
        main = MainPage(page)
        main.open()
        main.fill_from("Минск")
        main.fill_to("Москва")
        main.submit()

        expect(page).to_have_url(MainPage.URL, timeout=3000)

    @allure.story("Календарь")
    @allure.title("Прошедшие даты недоступны в календаре")
    def test_past_date_disabled_in_calendar(self, page):
        main = MainPage(page)
        main.open()
        yesterday = datetime.now() - timedelta(days=1)

        assert main.is_calendar_date_disabled(yesterday), \
            f"Ожидалось, что прошедшая дата ({yesterday.day}) будет недоступна в календаре"

    @allure.story("Автокомплит города")
    @allure.title("Ввод города — появляются подсказки")
    def test_city_autocomplete_shows_suggestions(self, page):
        main = MainPage(page)
        main.open()
        count = main.get_city_suggestions("Мин")

        assert count > 0, "Ожидались подсказки при вводе города 'Мин'"

    @allure.story("Автокомплит города")
    @allure.title("Несуществующий город — подсказок нет")
    def test_invalid_city_shows_no_suggestions(self, page):
        main = MainPage(page)
        main.open()
        count = main.get_city_suggestions("Хогвартс")

        assert count == 0, "Не ожидались подсказки для несуществующего города 'Хогвартс'"
