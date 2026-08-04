import pytest
from core.clients.api_client import APIClient
from datetime import datetime, timedelta
from faker import Faker
import random


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client

@pytest.fixture
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d")
    }

@pytest.fixture
def generate_random_booking_data(booking_dates):
    faker = Faker() # создаём объект класса Faker
    firstname = faker.first_name_nonbinary() # теперь пользуемся этим объектом
    lastname = faker.last_name_nonbinary()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()

    needs_options = [
        "sea view",
        "quiet room",
        "vegetarian meal",
        "late check-in requested",
        "non-smoking room",
        "baby crib needed",
        "high floor preferred",
        "extra pillows",
        "separate beds requested"
    ]

    additionalneeds = random.sample(needs_options, k=2) # 2 разных случайных элемента

    data = {
    "firstname": firstname,
    "lastname": lastname,
    "totalprice": totalprice,
    "depositpaid": depositpaid,
    "bookingdates": booking_dates,
    "additionalneeds": additionalneeds
    }

    return data

