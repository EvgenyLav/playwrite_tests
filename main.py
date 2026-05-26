import re
from playwright.sync_api import Playwright, sync_playwright, expect

from config import BASE_URL


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # --- Главная страница ---
    page.goto(BASE_URL)
    page.get_by_role("button", name="Согласен", exact=True).click()

    page.get_by_role("textbox", name="Пункт отправления").click()
    page.get_by_role("textbox", name="Пункт отправления").fill("Минск")
    page.get_by_role("textbox", name="Выберите пункт назначения").click()
    page.get_by_role("textbox", name="Выберите пункт назначения").fill("Москва")
    page.get_by_role("textbox", name="Выберите дату").click()
    page.get_by_role("button", name=re.compile(r"24 мая")).click()
    page.get_by_role("button", name="Найти билеты").click()

    # --- Страница результатов ---
    # Ждём загрузки карточек рейсов (implicit wait, без sleep)
    page.wait_for_selector("[class*='ListRatesItem']", timeout=20000)

    # Выбрать рейс 19:30 перевозчика Intercars
    page.locator("[class*='ListRatesItem_list-item__']").filter(
        has_text="19:30"
    ).filter(
        has_text="Intercars"
    ).get_by_role("button", name="Выбрать билет").first.click()

    # --- Страница бронирования ---
    # Ждём загрузки схемы мест, затем выбираем первое свободное
    page.wait_for_selector("[class*='BusTicket_free']", timeout=15000)
    page.locator("[class*='BusTicket_free']").first.click()

    # Заполнить данные пассажира
    page.locator("input[name='Passengers.1.LastName']").fill("Тест")
    page.locator("input[name='Passengers.1.FirstName']").fill("Тест")
    page.locator("input[name='Passengers.1.MiddleName']").fill("Тест")
    page.get_by_role("textbox", name="ДД.ММ.ГГГГ").fill("10.10.1993")

    # Гражданство
    page.locator("div").filter(has_text=re.compile(r"^Гражданство$")).nth(4).click()
    page.get_by_role("option", name="Беларусь").click()

    # Номер документа
    page.locator("input[name='Passengers.1.DocumentNumber']").fill("124124124РВ3")

    # Контакты — press_sequentially для маскированного поля телефона
    page.locator("input[name='Phone']").click()
    page.locator("input[name='Phone']").press_sequentially("2123231213")
    page.get_by_test_id("email").click()
    page.get_by_test_id("email").fill("test@test.ru")

    # Согласие
    page.get_by_test_id("termsAcceptedPolity").check()
    page.get_by_test_id("termsAcceptedProcessing").check()

    page.get_by_role("button", name="Оформить билет").click()

    # --- Платёжная страница ---
    page.get_by_role("button", name="Оплатить").click()

    # --- Платёжная страница ---
    page.wait_for_url(re.compile(r"abby\.rbsuat\.com"), timeout=10000)

    page.get_by_role("textbox", name="0000 0000 0000").fill("4111 1111 1111 1111")
    page.get_by_role("textbox", name="/00").fill("12/34")
    page.get_by_role("textbox", name="000", exact=True).fill("123")
    page.locator("[data-test-id='submitPayByCardForm']").click()

    page.get_by_role("textbox", name="Пароль").press_sequentially("12345678", delay=300)

    # --- Результат ---
    page.wait_for_url(re.compile(r"intercars-tickets\.com"), timeout=30000)
    expect(
        page.get_by_role("heading", name="Платеж не прошел")
        .or_(page.get_by_role("heading", name="Билет оформлен"))
    ).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)