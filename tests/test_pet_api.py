import time

import pytest

from src.factories.file_factory import FileFactory
from src.factories.pet_factory import UpdatePetFactory
from tests.conftest import pet_payload
from utils.checking_methods import Checking
from utils.enums import PetStatus
from utils.waiters import PetWaiter


def test_add_pet(pet_api, pet_payload):
    add_pet_response = pet_api.add_pet(pet_payload)
    assert add_pet_response.status_code == 200, f"unsuccessful attempt to add a pet"

    pet_data = add_pet_response.json()
    for key in ["id", "category", "name", "photoUrls", "tags", "status"]:
        assert key in pet_data, f"Missing key in response: {key}"
    assert (
        pet_data["status"] == pet_payload["status"]
    ), f"Expected status '{pet_payload['status']}', but got '{pet_data['status']}' for pet {pet_data['name']}"

    assert (
        pet_data["name"] == pet_payload["name"]
    ), f"Expected name: {pet_payload['name']}, got {pet_data['name']}"

    assert (
        pet_data["category"]["name"] == pet_payload["category"]["name"]
    ), f"Expected category id: '{pet_data['category']['id']}', but got '{pet_payload['category']['id']}'"

    assert isinstance(pet_data["id"],int)
    assert pet_data["name"], f"Pet name should not be empty"
# formated_pet_data=json.dumps(pet_data,indent=2)
# print(formated_pet_data)


def test_update_pet(pet_api, pet_payload):
    creating_pet_response = pet_api.add_pet(pet_payload)
    original_pet_data = dict(creating_pet_response.json())

    update_fields = UpdatePetFactory.update_pet_with_name_and_status(
        name="Alfredicus", status="sold"
    )

    copied_pet_data = original_pet_data.copy()
    copied_pet_data.update(update_fields)
    updated_pet = pet_api.update_pet(copied_pet_data)

    Checking.check_status_code(response=updated_pet, status_code=200)
    Checking.check_json_value(
        response=updated_pet, field_name="status", expected_value="sold"
    )
    Checking.check_json_value(
        response=updated_pet, field_name="name", expected_value="Alfredicus"
    )
    Checking.check_json_answer(
        response=updated_pet,
        expected_value=["id", "category", "name", "photoUrls", "tags", "status"],
    )


def test_get_pets_by_status(pet_api, pet_payload):
    find_pet_by_response = pet_api.find_pet_by_status(status=PetStatus.AVAILABLE)

    Checking.check_status_code(response=find_pet_by_response, status_code=200)
    Checking.check_json_value(
        response=find_pet_by_response, field_name="status", expected_value="available"
    )
    Checking.check_json_answer(
        response=find_pet_by_response,
        expected_value=["id", "name", "photoUrls", "tags", "status"],
    )


def test_find_pet_by_id(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)

    created_pet = creating_pet.json()
    pet_id = created_pet["id"]

    looking_pet_by_id = PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)

    Checking.check_status_code(response=looking_pet_by_id, status_code=200)
    Checking.check_json_value(
        response=looking_pet_by_id, field_name="status", expected_value="available"
    )
    Checking.check_json_answer(
        response=looking_pet_by_id,
        expected_value=["id", "name", "photoUrls", "tags", "status"],
    )


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_update_pet_with_form(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)
    time.sleep(3)
    created_pet = creating_pet.json()
    pet_id = created_pet["id"]

    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)
    response_with_update = pet_api.update_pet_with_form_data(
        pet_id, name="Lopik", status="sold"
    )

    Checking.check_status_code(response=response_with_update, status_code=200)
    Checking.check_json_value(
        response=response_with_update, field_name="message", expected_value=str(pet_id)
    )


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_delete_pet(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)
    Checking.check_status_code(creating_pet, 200)

    pet_id = creating_pet.json()["id"]
    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)
    delete_response = pet_api.delete_pet(pet_id)

    Checking.check_status_code(response=delete_response, status_code=[200, 204, 404])
    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=404)


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_upload_pet_image(pet_payload, files_client, pet_api):
    creating_pet = pet_api.add_pet(pet_payload)
    Checking.check_status_code(response=creating_pet, status_code=200)

    created_pet = creating_pet.json()
    pet_id = created_pet["id"]
    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)

    image_path = "test_dog.png"
    file_path = FileFactory.pet_image(image_path)

    response = files_client.upload_pet_image(pet_id=pet_id, file_path=file_path)

    Checking.check_status_code(response, 200)
