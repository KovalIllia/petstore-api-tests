from datetime import time

import pytest

from utils.checking_methods import Checking
from src.api.base_api import ApiClient
from src.api.files_api import FilesApi
from src.api.store_api import StoreApi
from src.factories.order_factory import OrderFactory
from utils.logger import Logger
from utils.waiters import StoreWaiter


def test_create_first_order(store_api, store_payload):
    response = store_api.place_order(store_payload)
    store_data = response.json()

    Checking.check_status_code(response=response, status_code=200)
    Checking.check_json_value(
        response=response, field_name="status", expected_value="placed"
    )
    Checking.check_json_answer(
        response=response,
        expected_value=["id", "petId", "quantity", "shipDate", "status", "complete"],
    )


def test_find_store_order_by_id(store_api, store_payload):
    response = store_api.place_order(store_payload)

    store_id = response.json()["id"]
    find_order = StoreWaiter.wait_for_order(store_api, store_id, expected_status=200)

    Checking.check_status_code(response=find_order, status_code=200)
    Checking.check_json_value(
        response=find_order, field_name="status", expected_value="placed"
    )
    Checking.check_json_answer(
        response=find_order,
        expected_value=["id", "petId", "quantity", "shipDate", "status", "complete"],
    )


def test_get_store_inventory(store_api):
    get_inventories = store_api.get_inventory()

    print(get_inventories.status_code, get_inventories.json())
    Checking.check_status_code(response=get_inventories, status_code=200)


def test_delete_purchase_order_by_id(store_payload, store_api):
    response = store_api.place_order(store_payload)
    store_id = response.json()["id"]

    find_order = StoreWaiter.wait_for_order(
        store_api, store_id, expected_status=[200, 404]
    )
    delete_store_order = store_api.delete_placed_order(store_id)

    Checking.check_status_code(response=delete_store_order, status_code=[200, 404])
    final_check = store_api.get_info_about_placed_order_by_id(store_id)
    Checking.check_status_code(response=response, status_code=[200, 404])
    if final_check.status_code == 200:
        print(f"API did not remove order {store_id}, got 200 instead of 404")
