import re
from dataclasses import replace

import allure
import pytest
from playwright.sync_api import expect

from pages.booking_page import BookingPage
from pages.main_page import MainPage
from pages.results_page import ResultsPage


@pytest.fixture
def booking_page(page, trip):
    """Navigates the full flow to the booking page with a seat selected."""
    main = MainPage(page)
    main.open()
    main.search(trip.from_city, trip.to_city, trip.days_offset)

    results = ResultsPage(page)
    results.wait_for_results()
    results.select_trip(trip.departure_time, trip.carrier)

    booking = BookingPage(page)
    booking.select_first_free_seat()
    return booking


@allure.epic("Бронирование билетов")
@allure.feature("Валидация формы бронирования")
@allure.severity(allure.severity_level.NORMAL)
class TestBookingValidation:

    @allure.story("Обязательные поля")
    @allure.title("Сабмит пустой формы — показываются ошибки обязательных полей")
    def test_empty_form_shows_errors(self, page, booking_page):
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_validation_errors(), \
            "Ожидались ошибки валидации после сабмита пустой формы"

    @allure.story("Формат email")
    @allure.title("Некорректный email — поле подсвечивается ошибкой")
    def test_invalid_email_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(passenger)
        booking_page.fill_phone(passenger.phone_digits)
        booking_page.accept_terms()
        booking_page.fill_email("notanemail")
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_email_error(), \
            "Ожидалась ошибка поля email при вводе некорректного значения 'notanemail'"

    @allure.story("Условия соглашения")
    @allure.title("Сабмит без принятия условий — остаёмся на странице бронирования")
    def test_submit_without_terms(self, page, booking_page, passenger):
        booking_page.fill_passenger(passenger)
        booking_page.fill_contacts(passenger)
        # условия намеренно не принимаются
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)

    @allure.story("Обязательные поля")
    @allure.title("Пустая фамилия — показывается ошибка поля фамилии")
    def test_missing_last_name_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(replace(passenger, last_name=""))
        booking_page.fill_contacts(passenger)
        booking_page.accept_terms()
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_last_name_error(), \
            "Ожидалась ошибка поля 'Фамилия' при пустом значении"

    @allure.story("Обязательные поля")
    @allure.title("Пустое имя — показывается ошибка поля имени")
    def test_missing_first_name_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(replace(passenger, first_name=""))
        booking_page.fill_contacts(passenger)
        booking_page.accept_terms()
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_first_name_error(), \
            "Ожидалась ошибка поля 'Имя' при пустом значении"

    @allure.story("Обязательные поля")
    @allure.title("Пустая дата рождения — показывается ошибка поля даты рождения")
    def test_missing_dob_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(replace(passenger, dob=""))
        booking_page.fill_contacts(passenger)
        booking_page.accept_terms()
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_dob_error(), \
            "Ожидалась ошибка поля 'Дата рождения' при пустом значении"

    @allure.story("Обязательные поля")
    @allure.title("Без телефона — показывается ошибка поля телефона")
    def test_missing_phone_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(passenger)
        booking_page.fill_email(passenger.email)
        booking_page.accept_terms()
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_phone_error(), \
            "Ожидалась ошибка поля 'Телефон' при незаполненном номере"

    @allure.story("Обязательные поля")
    @allure.title("Без email — показывается ошибка поля email")
    def test_missing_email_shows_error(self, page, booking_page, passenger):
        booking_page.fill_passenger(passenger)
        booking_page.fill_phone(passenger.phone_digits)
        booking_page.accept_terms()
        booking_page.submit()

        expect(page).to_have_url(re.compile(r"/booking\?id="), timeout=3000)
        assert booking_page.has_email_error(), \
            "Ожидалась ошибка поля 'Email' при незаполненном значении"
