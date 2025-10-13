import pytest

from conftest import pet_api
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

    assert isinstance(pet_data["id"], int)
    assert pet_data["name"], f"Pet name should not be empty"


def test_update_pet(pet_api, pet_payload):
    add_pet_response = pet_api.add_pet(pet_payload)
    assert add_pet_response.status_code == 200, f"unsuccessful attempt to create a pet"
    original_pet_data = dict(add_pet_response.json())

    update_fields = UpdatePetFactory.update_pet_with_name_and_status(
        name="Alfredicus", status="sold"
    )
    copied_pet_data = original_pet_data.copy()
    for key in ["id", "category", "name", "photoUrls", "tags", "status"]:
        assert key in copied_pet_data, f"Missing key in response: {copied_pet_data}"
    copied_pet_data.update(update_fields)
    updated_pet = pet_api.update_pet(copied_pet_data)
    assert (
        updated_pet.status_code == 200
    ), f"Update failed, got {updated_pet.status_code}:{updated_pet.text}"

    updated_pet_data = updated_pet.json()
    assert (
        updated_pet_data["name"] == update_fields["name"]
    ), f"Expected name: {update_fields['name']}, got {updated_pet_data['name']}"
    assert (
        updated_pet_data["status"] == update_fields["status"]
    ), f"Expected name: {update_fields['status']}, got {updated_pet_data['status']}"


def test_get_pets_by_status(pet_api, pet_payload):
    find_pet_by_response = pet_api.find_pet_by_status(status=PetStatus.AVAILABLE)
    assert (
        find_pet_by_response.status_code == 200
    ), f"unsuccessful attempt to get a pet by status"
    pets_data = find_pet_by_response.json()

    assert isinstance(pets_data, list), f"Expected list of pets"
    assert len(pets_data) > 0, f"Empty list of pets"

    for pet in pets_data:
        assert "status" in pet, f"Missing key 'status' in pet: {pet}"


def test_find_pet_by_id(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)
    assert creating_pet.status_code == 200, f"unsuccessful attempt to create a pet"

    created_pet = creating_pet.json()
    assert isinstance(created_pet, dict), f"Expected list of pets"
    assert len(created_pet) > 0, f"Empty list of pets"
    print(f"Sent ID: {pet_payload['id']}, received ID: {created_pet['id']}")


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_update_pet_with_form(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)
    assert creating_pet.status_code == 200, f"unsuccessful attempt to add a pet"

    created_pet_data = creating_pet.json()
    pet_id = created_pet_data["id"]

    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)

    new_name = "Lopik"
    new_status = "sold"

    response_with_update = pet_api.update_pet_with_form_data(
        pet_id, new_name, new_status
    )
    assert (
        response_with_update.status_code == 200
    ), f"Form update failed: {response_with_update.text}"

    response_with_update_data = response_with_update.json()

    assert (
        "message" in response_with_update_data
    ), f"No 'message' in form update response: {response_with_update_data}"
    assert (
        str(pet_id) in response_with_update_data["message"]
    ), f"Wrong pet ID in response message: {response_with_update_data}"

    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)

    get_pet_by_id = pet_api.find_pet_by_id(pet_id)
    assert get_pet_by_id.status_code == 200, f"unsuccessful attempt to find a pet by id"

    updated_pet_data = get_pet_by_id.json()
    assert (
        updated_pet_data["name"] == new_name
    ), f"expected name: {new_name}, but got: {updated_pet_data['name']} "
    assert (
        updated_pet_data["status"] == new_status
    ), f"expected name: {new_status}, but got: {updated_pet_data['status']} "


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_delete_pet(pet_api, pet_payload):
    creating_pet = pet_api.add_pet(pet_payload)
    assert creating_pet.status_code == 200, f"unsuccessful attempt to add a pet"

    pet_id = creating_pet.json()["id"]
    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)
    delete_response = pet_api.delete_pet(pet_id)
    assert delete_response.status_code == 200, f"unsuccessful attempt to delete a pet"

    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=404)
    found_animal_response = pet_api.find_pet_by_id(pet_id)
    assert (
        found_animal_response.status_code == 404
    ), f"Pet with id: {pet_id} was not deleted"


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_upload_pet_image(pet_payload, files_client, pet_api):
    creating_pet = pet_api.add_pet(pet_payload)
    assert creating_pet.status_code == 200, f"unsuccessful attempt to add a pet"

    created_pet = creating_pet.json()
    pet_id = created_pet["id"]
    PetWaiter.wait_for_pet(pet_api, pet_id, expected_status=200)

    image_path = "test_dog.png"
    file_path = FileFactory.pet_image(image_path)

    response = files_client.upload_pet_image(pet_id=pet_id, file_path=file_path)
    assert response.status_code == 200, f"unsuccessful to upload pet image"
    upload_data = response.json()
    assert (
        "message" in upload_data
    ), f"No 'message' in form update response: {upload_data}"
    for key in ["code", "type", "message"]:
        assert key in upload_data, f"Missing {key} in response: {upload_data}"

    get_response = pet_api.find_pet_by_id(pet_id)
    assert get_response.status_code == 200, f"Failed to get pet after image upload"
    pet_data_after_upload = get_response.json()
    assert (
        len(pet_data_after_upload["photoUrls"]) > 0
    ), "photoUrls is empty after image upload"
