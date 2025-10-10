from enum import Enum


class PetStatus(Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


print(PetStatus.AVAILABLE)
