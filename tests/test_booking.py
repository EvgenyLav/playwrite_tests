import re

import allure
import pytest

from config import TEST_CARD
from pages.booking_page import BookingPage
from pages.main_page import MainPage
from pages.payment_page import PaymentPage
from pages.pre_payment_page import PrePaymentPage
from pages.results_page import ResultsPage


@allure.epic("Бронирование билетов")
@allure.feature("Оформление заказа")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_booking(page, passenger, trip):
    allure.dynamic.title(f"Смоук: бронирование {trip}")
    allure.dynamic.story(f"{trip.from_city} → {trip.to_city}")

    # Шаг 1: Поиск
    main = MainPage(page)
    main.open()
    search_date = main.search(trip.from_city, trip.to_city, trip.days_offset)

    # Шаг 2: Результаты — маршрут, дата и цена совпадают с поисковым запросом
    results = ResultsPage(page)
    results.wait_for_results()

    heading = results.get_route_heading()
    assert trip.from_city in heading and trip.to_city in heading, \
        f"Маршрут не совпадает: ожидался '{trip.from_city}→{trip.to_city}', получили '{heading}'"

    displayed_dates = results.get_displayed_dates()
    assert len(displayed_dates) > 0, "Результаты поиска пусты — ни одного рейса не загружено"
    expected_date = search_date.strftime("%d.%m")
    assert any(expected_date in d for d in displayed_dates), \
        f"Дата '{expected_date}' не найдена среди дат рейсов: {displayed_dates}"

    assert results.trip_exists(trip.departure_time, trip.carrier), \
        f"Рейс {trip.departure_time} {trip.carrier} не найден в результатах поиска"

    price = results.get_price(trip.departure_time, trip.carrier)
    assert re.search(r"\d+", price), f"Цена не содержит числа: '{price}'"

    results.select_trip(trip.departure_time, trip.carrier)

    # Шаг 3: Бронирование — цена не изменилась, данные пассажира заполнены
    booking = BookingPage(page)
    booking.select_first_free_seat()
    booking.fill_passenger(passenger)
    booking.fill_contacts(passenger)

    booking_price = booking.get_total_price()
    assert booking_price == price, \
        f"Цена изменилась на шаге бронирования: '{booking_price}' ≠ '{price}'"

    booking.accept_terms()
    booking.submit()

    # Шаг 4: Подтверждение — данные пассажира и цена совпадают с введёнными
    pre_payment = PrePaymentPage(page)
    pre_payment.wait_for_page()

    assert pre_payment.has_passenger_name(passenger.full_name), \
        f"ФИО '{passenger.full_name}' не найдено на странице подтверждения"
    assert pre_payment.has_email(passenger.email), \
        f"Email '{passenger.email}' не найден на странице подтверждения"
    assert pre_payment.has_text(trip.departure_time), \
        f"Время отправления '{trip.departure_time}' не отображается на странице подтверждения"
    assert pre_payment.has_text(trip.carrier), \
        f"Перевозчик '{trip.carrier}' не отображается на странице подтверждения"
    assert pre_payment.has_text(trip.from_city) and pre_payment.has_text(trip.to_city), \
        f"Маршрут '{trip.from_city}→{trip.to_city}' не отображается на странице подтверждения"

    prepayment_price = pre_payment.get_total_price()
    assert prepayment_price == price, \
        f"Цена изменилась перед оплатой: '{prepayment_price}' ≠ '{price}'"

    pre_payment.pay()

    # Шаг 5: Оплата
    payment = PaymentPage(page)
    payment.fill_card(TEST_CARD.number, TEST_CARD.expiry, TEST_CARD.cvv)
    payment.submit_3ds(TEST_CARD.password_3ds)
    # Редирект после 3DS проходит, но билет не создаётся из-за бага API
