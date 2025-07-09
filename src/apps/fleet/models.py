from django.db import models

from lib.helpers.behaviors import BaseModelable


class Car(BaseModelable, models.Model):

    make = models.CharField(verbose_name="Vehicle manufacturer", max_length=20)
    model = models.CharField(verbose_name="Vehicle model", max_length=20)
    year = models.IntegerField(verbose_name="Vehicle model year")


class Driver(BaseModelable, models.Model):

    name = models.CharField(verbose_name="Driver name", max_length=255)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, related_name="driver", null=True, blank=True)
    is_available = models.BooleanField(verbose_name="Is Available", default=True)
