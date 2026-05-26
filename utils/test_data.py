from dataclasses import dataclass
from faker import Faker

fake = Faker("ru_RU")


@dataclass
class PassengerData:
    last_name: str
    first_name: str
    middle_name: str
    dob: str
    citizenship: str
    doc_number: str
    phone_digits: str
    email: str

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"


@dataclass
class TripData:
    from_city: str
    to_city: str
    departure_time: str
    carrier: str
    days_offset: int = None

    def __str__(self) -> str:
        return f"{self.from_city}→{self.to_city} {self.departure_time} {self.carrier}"


def generate_passenger() -> PassengerData:
    # Дата рождения: возраст 27–59 лет (тариф РТ)
    dob = fake.date_of_birth(minimum_age=27, maximum_age=59)
    doc_number = fake.numerify("#######") + "РВ3"

    # Поле телефона с маской +1 (US по умолчанию) — вводим 10 цифр
    phone_digits = fake.numerify("##########")

    return PassengerData(
        last_name=fake.last_name_male(),
        first_name=fake.first_name_male(),
        middle_name=fake.middle_name_male(),
        dob=dob.strftime("%d.%m.%Y"),
        citizenship="Беларусь",
        doc_number=doc_number,
        phone_digits=phone_digits,
        email=fake.email(),
    )
