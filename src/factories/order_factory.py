import random
import datetime


class OrderFactory:
    @staticmethod
    def default_order(
        id: int = None,
        petId: int = None,
        quantity: int = 1,
        shipDate: str = None,
        status: str = "placed",
        complete: bool = True,
    ) -> dict:

        if id is None:
            id = random.randint(1, 10000)
        if petId is None:
            petId = random.randint(1, 10000)
        if shipDate is None:
            shipDate = datetime.datetime.now().isoformat()

        body = {
            "id": id,
            "petId": petId,
            "quantity": quantity,
            "shipDate": shipDate,
            "status": status,
            "complete": complete,
        }
        return body
