from typing import Dict

from faker import Faker
from faker_vehicle import VehicleProvider

from apps.fleet.models import Car

Faker.seed(0)
fake = Faker(["es_CO"])
fake.add_provider(VehicleProvider)


def fake_car() -> Dict[str, str]:
    """
    Generates fake car data.

    Returns:
        A dictionary containing fake 'make', 'model', and 'year' for a car.
    """

    return {
        "make": fake.vehicle_make()[:19],
        "model": fake.vehicle_model()[:19],
        "year": fake.random.randint(1990, 2026),
    }


def fake_driver(car: Car) -> Dict[str, str]:
    """
    Generates fake driver data.

    Args:
        car: A Car instance to associate with the driver.

    Returns:
        A dictionary containing fake 'name', the associated 'car' object, and 'is_available' status for a driver.
    """
    return {"name": fake.name(), "car": car, "is_available": True}
