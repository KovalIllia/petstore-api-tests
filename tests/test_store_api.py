import pytest

from utils.waiters import StoreWaiter


def test_create_first_order(store_api, store_payload):
    create_order_response = store_api.place_order(store_payload)
    assert create_order_response.status_code == 200, f"unsuccessful attempt to create an order"
    store_data = create_order_response.json()
    assert isinstance(store_data, dict), f"Expected disct of pets"
    assert len(store_data) > 0, f"Empty dict of pets"
    for key in ["id", "petId", "quantity", "shipDate", "status", "complete"]:
        assert key in store_data, f"Missing key in response: {key}"
    assert store_data["id"] == store_payload["id"], f"Wrong pet ID in response message: {store_data}"
    assert store_data["petId"] == store_payload["petId"], f"Wrong pet ID in response message: {store_data}"
    print(store_data)


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.unstable(reason="Petstore API sometimes returns 404 after order creation")
def test_find_store_order_by_id(store_api, store_payload):
    create_order_response = store_api.place_order(store_payload)
    assert create_order_response.status_code == 200, f"unsuccessful attempt to create an order"

    store_data = create_order_response.json()
    assert isinstance(store_data, dict), "Expected dict of pets"
    assert len(store_data) > 0, "Empty order data"
    order_id = store_data["id"]
    assert order_id is not None, "Order ID should not be None"
    StoreWaiter.wait_for_order(store_api, order_id, expected_status=200)
    find_order = store_api.get_info_about_placed_order_by_id(order_id)
    assert find_order.status_code == 200, f"Failed to get order by : {order_id}"
    find_order_data = find_order.json()
    for key in ["id", "petId", "quantity", "shipDate", "status", "complete"]:
        assert key in find_order_data, f"Missing {key} in found order: {find_order_data}"
    assert find_order_data["id"] == store_data[
        "id"], f"Expected id: {store_data['id']}, but got {find_order_data['id']}"
    assert find_order_data["petId"] == store_data[
        "petId"], f"Expected petId: {store_data['petId']}, but got {find_order_data['petId']}"


def test_get_store_inventory(store_api):
    get_inventories = store_api.get_inventory()
    get_inventories_data = get_inventories.json()
    assert get_inventories.status_code == 200, f"unsuccessful to get information about inventory"
    assert isinstance(get_inventories_data, dict), "unsuccessful attempt to get pet inventories by status"
    assert len(get_inventories_data) > 0, "Empty inventories data"
    assert len(
        str(get_inventories_data["available"])) > 0, f"Quantity should be > 0, got {get_inventories_data['available']}"

@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_delete_purchase_order_by_id(store_payload, store_api):
    create_order_response = store_api.place_order(store_payload)
    assert create_order_response.status_code == 200, f"unsuccessful attempt to create an order"
    store_data=create_order_response.json()
    store_id = store_data["id"]

    StoreWaiter.wait_for_order(
        store_api, store_id, expected_status=[200, 404]
    )
    delete_store_order = store_api.delete_placed_order(store_id)
    assert (
            delete_store_order.status_code == 200
    ), f"unsuccessful attempt to delete store: {store_id}"
    StoreWaiter.wait_for_order(
        store_api, store_id, expected_status=[404]
    )
    found_deleted_data = store_api.get_info_about_placed_order_by_id(store_id)
    assert (
            found_deleted_data.status_code == 404
    ), f"Pet with id: {store_id} was not deleted"

    # Checking.check_status_code(response=delete_store_order, status_code=[200, 404])
    # final_check = store_api.get_info_about_placed_order_by_id(store_id)
    # Checking.check_status_code(response=response, status_code=[200, 404])
    # if final_check.status_code == 200:
    #     print(f"API did not remove order {store_id}, got 200 instead of 404")
