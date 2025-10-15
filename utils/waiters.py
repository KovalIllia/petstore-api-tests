import time


class PetWaiter:
    @staticmethod
    def wait_for_pet(pet_api, pet_id: int, expected_status=200, retries=20, delay=3):
        last_status = None

        for attempt in range(1, retries + 1):
            try:
                response = pet_api.find_pet_by_id(pet_id)
                last_status = response.status_code

                print(f"🔄 Attempt {attempt}/{retries} - Status: {response.status_code}")

                if response.status_code == expected_status:
                    print(f"✅ Pet {pet_id} is available")
                    return response
                elif response.status_code == 404:
                    """handling 404 as a temporary error"""
                    print(f"⚠️Pet {pet_id} not found (attempt {attempt}), continuing...")
                else:
                    print(f"❌ Unexpected status: {response.status_code}")

            except Exception as e:
                print(f"⚠️Error in attempt {attempt}: {e}")

            time.sleep(delay)

        """IMPROVED bug: taking into account API instability"""
        raise AssertionError(
            f"Pet {pet_id} not consistently available after {retries} retries. "
            f"API is unstable - last status: {last_status}. "
            f"This is expected behavior for test Petstore environment."
        )

class StoreWaiter:
    @staticmethod
    def wait_for_order(
        store_api, order_id: int, expected_status=200, retries= 20, delay= 4):
        """
        Waits for order until its status code matches expected_status.
        Supports single int or list/tuple of acceptable statuses.
        """
        for attempt in range(1, retries + 1):
            response = store_api.get_info_about_placed_order_by_id(order_id)

            if isinstance(expected_status, (list, tuple)):
                if response.status_code in expected_status:
                    return response
            else:
                if response.status_code == expected_status:
                    return response

            print(
                f"[Retry {attempt}] Order {order_id} not found, got {response.status_code}"
            )
            time.sleep(delay)

        raise AssertionError(
            f"Order {order_id} not found after {retries} attempts. "
            f"Expected {expected_status}, got last {response.status_code}"
        )

"""Temporary"""
class UpdateWaiter:
    """Special Waiter for update operations with unstable API"""

    @staticmethod
    def wait_for_update_success(pet_api, pet_id: int, update_func, *args, **kwargs):
        max_retries = 5

        for attempt in range(1, max_retries + 1):
            print(f"🔄 Update attempt {attempt}/{max_retries} for pet {pet_id}")
            """do updating"""
            response = update_func(*args, **kwargs)

            if response.status_code == 200:
                print(f"✅ Update successful on attempt {attempt}")
                return response
            elif response.status_code == 404:
                print(f"⚠️ Update failed with 404 (attempt {attempt}), retrying...")
                time.sleep(2)
            else:
                print(f"❌ Update failed with status {response.status_code}")
                return response

        raise AssertionError(f"Update failed after {max_retries} attempts due to API instability")