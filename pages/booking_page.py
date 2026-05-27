import re

import allure
from playwright.sync_api import Page

from utils.test_data import PassengerData


class BookingPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Выбрать первое свободное место")
    def select_first_free_seat(self):
        self.page.locator("[class*='BusTicket_free']").first.click(timeout=15000)

    @allure.step("Заполнить данные пассажира")
    def fill_passenger(self, passenger: PassengerData):
        self.page.locator("input[name='Passengers.1.LastName']").fill(passenger.last_name)
        self.page.locator("input[name='Passengers.1.FirstName']").fill(passenger.first_name)
        self.page.locator("input[name='Passengers.1.MiddleName']").fill(passenger.middle_name)
        self.page.get_by_role("textbox", name="ДД.ММ.ГГГГ").fill(passenger.dob)
        self.page.locator("div").filter(has_text=re.compile(r"^Гражданство$")).nth(4).click()
        self.page.get_by_role("option", name=passenger.citizenship).click()
        self.page.locator("input[name='Passengers.1.DocumentNumber']").fill(passenger.doc_number)

    @allure.step("Заполнить контактные данные")
    def fill_contacts(self, passenger: PassengerData):
        self.fill_phone(passenger.phone_digits)
        self.fill_email(passenger.email)

    @allure.step("Заполнить номер телефона")
    def fill_phone(self, digits: str):
        phone = self.page.locator("input[name='Phone']")
        phone.click()
        phone.press_sequentially(digits)

    @allure.step("Заполнить email {email}")
    def fill_email(self, email: str):
        self.page.get_by_test_id("email").fill(email)

    def has_validation_errors(self) -> bool:
        return self.page.locator("[class*='error']").filter(
            has_text=re.compile(r"\S")
        ).count() > 0

    def _field_has_error(self, field_locator) -> bool:
        error = self.page.locator("[class*='error']").filter(has_text=re.compile(r"\S"))
        return self.page.locator("div").filter(
            has=field_locator
        ).filter(has=error).count() > 0

    def has_last_name_error(self) -> bool:
        return self._field_has_error(self.page.locator("input[name='Passengers.1.LastName']"))

    def has_first_name_error(self) -> bool:
        return self._field_has_error(self.page.locator("input[name='Passengers.1.FirstName']"))

    def has_dob_error(self) -> bool:
        return self._field_has_error(self.page.get_by_role("textbox", name="ДД.ММ.ГГГГ"))

    def has_phone_error(self) -> bool:
        return self._field_has_error(self.page.locator("input[name='Phone']"))

    def has_email_error(self) -> bool:
        return self._field_has_error(self.page.get_by_test_id("email"))

    @allure.step("Получить итоговую стоимость на странице бронирования")
    def get_total_price(self) -> str:
        el = self.page.locator("[class*='price']").filter(
            has_text=re.compile(r"\d+\s*(?:EUR|BYN|USD|руб|₽)")
        ).first
        text = el.text_content()
        match = re.search(r"\d[\d\s.,]*(?:EUR|BYN|USD|руб|₽)", text)
        return match.group().strip() if match else text.strip()

    @allure.step("Принять условия соглашения")
    def accept_terms(self):
        self.page.get_by_test_id("termsAcceptedPolity").check(force=True)
        self.page.get_by_test_id("termsAcceptedProcessing").check(force=True)

    @allure.step("Нажать 'Оформить билет'")
    def submit(self):
        self.page.get_by_role("button", name="Оформить билет").click()
