import os
import requests
import allure
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Credentials, Timeouts
from requests.auth import HTTPBasicAuth

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json"
        }


    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment: {environment}")


    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.session.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()


    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.session.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()


    @allure.title("Checking service availability")
    def ping(self):
        with allure.step('Ping API client'):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code


    @allure.title("Get auth token")
    def auth(self):
        with allure.step('Get authenticate'):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {
                "username": Credentials.USERNAME.value,
                "password": Credentials.PASSWORD.value
            }
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step('Checking token'):
            assert token, f"Token is missing in response"
        with allure.step('Updating header with token'):
            self.session.headers.update({"Authorization": f"Bearer {token}"})


    @allure.title("Get booking by id")
    def get_booking_by_id(self, booking_id):
        with allure.step('Make a request to get booking by id'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


    @allure.title("Delete booking")
    def delete_booking(self, booking_id):
        with allure.step('Booking deletion'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Credentials.USERNAME.value, Credentials.PASSWORD.value))
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code == 201


    @allure.title("Update booking")
    def update_booking(self, booking_id, booking_data):
        with allure.step('Booking updating'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, auth=HTTPBasicAuth(Credentials.USERNAME.value, Credentials.PASSWORD.value), json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


    @allure.title("Create booking")
    def create_booking(self, booking_data):
        with allure.step('Booking creating'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"

            # response = self.session.post(url, json=booking_data)

            response = requests.post(
                url,
                json=booking_data,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


    @allure.title("Partial update booking")
    def partial_update_booking(self, booking_id, booking_data):
        with allure.step('Booking partial updating'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, auth=HTTPBasicAuth(Credentials.USERNAME.value, Credentials.PASSWORD.value), json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


    @allure.title("Get booking ids")
    def get_booking_ids(self, params=None):
        with allure.step('Getting object with bookings'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()
