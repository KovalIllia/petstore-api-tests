import random
import uuid

from faker import Faker

fake = Faker()


class PetFactory:
    @staticmethod
    def default_pet(name=None, status="available") -> dict:
        return {
            "id": uuid.uuid4().int & (1 << 31) - 1,  # Unique id + character limit
            "category": {"id": uuid.uuid4().int & (1 << 31) - 1, "name": fake.word()},
            "name": name or fake.first_name(),
            "photoUrls": [fake.image_url()],
            "tags": [{"id": uuid.uuid4().int & (1 << 31) - 1, "name": fake.word()}],
            "status": status,
        }


class UpdatePetFactory:
    @staticmethod
    def update_pet_with_name_and_status(name: str = None, status: str = None) -> dict:
        body = {}
        if name:
            body["name"] = name
        if status:
            body["status"] = status
        return body
