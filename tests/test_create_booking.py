import allure
import pytest


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
    with pytest.raises(AssertionError, match=f"Expected status code 200 but got 500"):
        api_client.create_booking(random_booking_data_with_none_totalprice)


@allure.feature("Test create booking")
@allure.story("Negative test: create booking without bookingdates")
def test_booking_without_bookingdates(api_client, random_booking_data_without_bookingdates):
    with pytest.raises(AssertionError, match=f"Expected status code 200 but got 500"):
        api_client.create_booking(random_booking_data_without_bookingdates)



