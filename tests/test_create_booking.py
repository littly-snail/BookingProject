import allure
import pytest
from requests.exceptions import HTTPError


@allure.feature("Test create booking")
@allure.story("Test create correct booking")
def test_correct_booking(api_client, generate_random_booking_data):
    b_json = api_client.create_booking(generate_random_booking_data)["booking"]
    assert b_json["firstname"] == generate_random_booking_data["firstname"], "Имя гостя не совпало с ожидаемым"
    assert b_json["lastname"] == generate_random_booking_data["lastname"], "Фамилия гостя не совпала с ожидаемой"
    assert b_json["totalprice"] == generate_random_booking_data["totalprice"], "Сумма бронирования не совпала с ожидаемой"
    assert b_json["depositpaid"] == generate_random_booking_data["depositpaid"], "Статус оплаты не совпал с ожидаемым"
    assert b_json["bookingdates"] == generate_random_booking_data["bookingdates"], "Даты бронирования не совпали с ожидаемыми"
    assert b_json["additionalneeds"] == generate_random_booking_data["additionalneeds"], "Доп.пожелания не совпали с ожидаемыми"


@allure.feature("Test create booking")
@allure.story("Negative test: create booking with None totalprice")
def test_booking_with_none_totalprice(api_client, random_booking_data_with_none_totalprice):
    with pytest.raises(HTTPError, match="500"):
        api_client.create_booking(random_booking_data_with_none_totalprice)


@allure.feature("Test create booking")
@allure.story("Negative test: create booking without bookingdates")
def test_booking_without_bookingdates(api_client, random_booking_data_without_bookingdates):
    with pytest.raises(HTTPError, match="500"):
        api_client.create_booking(random_booking_data_without_bookingdates)


# Checking that the extra field was ignored
@allure.feature("Test create booking")
@allure.story("Negative test: create booking with unexpected field")
def test_booking_with_unexpected_field(api_client, random_booking_data_with_unexpected_field):
    b_json = api_client.create_booking(random_booking_data_with_unexpected_field)["booking"]
    assert b_json["firstname"] == random_booking_data_with_unexpected_field["firstname"], "Имя гостя не совпало с ожидаемым"
    assert b_json["lastname"] == random_booking_data_with_unexpected_field["lastname"], "Фамилия гостя не совпала с ожидаемой"
    assert b_json["totalprice"] == random_booking_data_with_unexpected_field["totalprice"], "Сумма бронирования не совпала с ожидаемой"
    assert b_json["depositpaid"] == random_booking_data_with_unexpected_field["depositpaid"], "Статус оплаты не совпал с ожидаемым"
    assert b_json["bookingdates"] == random_booking_data_with_unexpected_field["bookingdates"], "Даты бронирования не совпали с ожидаемыми"
    assert b_json["additionalneeds"] == random_booking_data_with_unexpected_field["additionalneeds"], "Доп.пожелания не совпали с ожидаемыми"
    assert "unexpected_field" not in b_json, "unexpected_field не должен присутствовать в ответе"


# Checking that the create_booking can convert a sum with the string type and leading zeros to a number.
@allure.feature("Test create booking")
@allure.story("create booking, convert totalprice from a string to a number")
def test_booking_with_leading_zeros_totalprice(api_client, random_booking_data_with_leading_zeros_totalprice):
    b_json = api_client.create_booking(random_booking_data_with_leading_zeros_totalprice)["booking"]
    assert b_json["firstname"] == random_booking_data_with_leading_zeros_totalprice["firstname"], "Имя гостя не совпало с ожидаемым"
    assert b_json["lastname"] == random_booking_data_with_leading_zeros_totalprice["lastname"], "Фамилия гостя не совпала с ожидаемой"
    assert b_json["totalprice"] == int(random_booking_data_with_leading_zeros_totalprice["totalprice"]), "Сумма бронирования не совпала с ожидаемой"
    assert b_json["depositpaid"] == random_booking_data_with_leading_zeros_totalprice["depositpaid"], "Статус оплаты не совпал с ожидаемым"
    assert b_json["bookingdates"] == random_booking_data_with_leading_zeros_totalprice["bookingdates"], "Даты бронирования не совпали с ожидаемыми"
    assert b_json["additionalneeds"] == random_booking_data_with_leading_zeros_totalprice["additionalneeds"], "Доп.пожелания не совпали с ожидаемыми"
