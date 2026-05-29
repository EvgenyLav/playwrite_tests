import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ["BASE_URL"]


@dataclass(frozen=True)
class CardData:
    number: str
    expiry: str
    cvv: str
    password_3ds: str


TEST_CARD = CardData(
    number="4111 1111 1111 1111",
    expiry="12/34",
    cvv="123",
    password_3ds="12345678",
)


@dataclass(frozen=True)
class WebPayCardData:
    month: str
    year: str
    holder: str
    cvv: str
    email: str


WEBPAY_CARD = WebPayCardData(
    month="06",
    year="27",
    holder="TEST USER",
    cvv="123",
    email="test@test.com",
)
