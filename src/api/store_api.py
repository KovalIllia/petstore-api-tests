import allure

from src.api.base_api import ApiClient


class StoreApi:

    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("GET /store/inventory")
    def get_inventory(self):
        return self.client.get("/store/inventory")

    @allure.step("GET /store/order/order_id")
    def get_info_about_placed_order_by_id(self, order_id: int):
        return self.client.get(f"/store/order/{order_id}")

    @allure.step("POST /store/order")
    def place_order(self, body: dict):
        return self.client.post("/store/order", body)

    @allure.step("DELETE /store/order/order_id")
    def delete_placed_order(self, order_id: int):
        return self.client.delete(f"/store/order/{order_id}")
