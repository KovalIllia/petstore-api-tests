import datetime
import random

import allure
import requests


class ApiClient:

    def __init__(
        self,
        logger,
        base_url: str = "https://petstore.swagger.io/v2",
    ):
        self.base_url = base_url
        self.logger = logger

    # def build_url(self, resource: str) -> str:
    #     return f"{self.base_url}{resource}"

    def build_url(self, resource: str) -> str:
        return f"{self.base_url.rstrip('/')}/{resource.lstrip('/')}"

    def get(self, resource: str, params: dict = None) -> requests.Response:
        url = self.build_url(resource)
        self.logger.add_request(url, method="GET", body=params)
        response = requests.get(url)
        self.logger.add_response(response, body=params)
        return response

    def post(self, resource: str, body: dict) -> requests.Response:
        url = self.build_url(resource)
        self.logger.add_request(url, method="POST", body=body)
        response = requests.post(url, json=body)
        self.logger.add_response(response, body=body)
        return response

    def delete(self, resource: str, params: dict = None) -> requests.Response:
        url = self.build_url(resource)
        self.logger.add_request(url, method="DELETE", body=params)
        response = requests.delete(url)
        self.logger.add_response(response, body=params)
        return response

    def put(self, resource: str, body: dict) -> requests.Response:
        url = self.build_url(resource)
        self.logger.add_request(url, method="PUT", body=body)
        response = requests.put(url, json=body)
        self.logger.add_response(response, body=body)
        return response

    def post_form(self, resource: str, body: dict, headers: dict) -> requests.Response:
        url = self.build_url(resource)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.logger.add_request(url, method="POST", body=body)
        response = requests.post(url, data=body, headers=headers)
        self.logger.add_response(response, body=body)

        return response
