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
