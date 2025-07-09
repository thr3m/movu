import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from django.db import transaction

from apps.fleet.models import Car, Driver
from apps.fleet.helpers import faker
from apps.administration.models import User


@dataclass
class FakeInitData:
    """
    A utility class for generating and populating fake initial data for the fleet application.
    """
    def bulk_create(
        self,
        Model: Union[Car, Driver],
        fake_method: Callable,
        cars: Optional[List[Car]] = None,
        total_rows: int = 10,
    ):
        """
        Bulk creates instances of a given Django Model using a fake data generation method.

        Args:
            Model: The Django Model class (Car or Driver) to create instances for.
            fake_method: A callable function that generates fake data for the model.
            cars: Optional list of Car instances to associate with Driver instances.
            total_rows: The number of fake instances to create.
        """
        objs = []
        for _ in range(total_rows):
            if cars:
                data = fake_method(random.choice(cars))
            else:
                data = fake_method()

            objs.append(Model(**data))
        Model.objects.bulk_create(objs)

    def setup_car(self):
        """
        Sets up fake car data by bulk creating Car instances.
        """
        self.bulk_create(Model=Car, fake_method=faker.fake_car)

    def setup_driver(self, cars: List[Car]):
        """
        Sets up fake driver data by bulk creating Driver instances.

        Args:
            cars: A list of existing Car instances to associate with drivers.
        """
        self.bulk_create(Model=Driver, fake_method=faker.fake_driver, cars=cars)

    def setup_admin_user(self):
        """
        Ensures an admin user with username 'admin' exists. Creates one if it doesn't.
        """
        try:
            User.objects.get(username="admin")
        except User.DoesNotExist:
            User.objects.create_superuser(username="admin", email="admin@admin.com", password="admin123456")


@transaction.atomic
def run():
    """
    Main function to run the fake data initialization script.
    Creates fake cars, drivers, and an admin user.
    """
    fake = FakeInitData()

    fake.setup_car()
    cars = list(Car.objects.all())

    fake.setup_driver(cars)
    fake.setup_admin_user()
