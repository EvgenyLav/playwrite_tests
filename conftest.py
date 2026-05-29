from dataclasses import dataclass

import allure
import pytest

from config import TEST_CARD, WEBPAY_CARD
from pages.payment_page import PaymentPage
from pages.webpay_page import WebPayPage
from utils.test_data import generate_passenger, TripData


@dataclass
class PaymentScenario:
    selector: str
    page_class: type
    card: object

collect_ignore = ["tests/new_test.py"]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "headless": False}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


@pytest.fixture(autouse=True)
def set_timeouts(page):
    page.set_default_navigation_timeout(60000)


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name="Скриншот при падении",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.fixture
def passenger():
    return generate_passenger()


@pytest.fixture(
    params=[
        pytest.param(
            PaymentScenario(selector="alfaBank", page_class=PaymentPage, card=TEST_CARD),
            id="alfa-bank",
        ),
        pytest.param(
            PaymentScenario(selector="webPay", page_class=WebPayPage, card=WEBPAY_CARD),
            id="web-pay",
        ),
    ]
)
def payment_scenario(request):
    return request.param


@pytest.fixture(
    params=[
        pytest.param(
            TripData(from_city="Минск", to_city="Москва", departure_time="19:30", carrier="Intercars", days_offset=1),
            id="minsk-moscow-1930-intercars",
        ),
    ]
)
def trip(request):
    return request.param
