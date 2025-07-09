import uuid

from django.db import models

class Timestampable(models.Model):
    """
    An abstract base class model that provides self-managed `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField('created at',auto_now_add=True)
    updated_at = models.DateTimeField('last updated at',auto_now=True)

    class Meta:
        abstract = True

class BaseModelable(Timestampable):
    """
    An abstract base class model that provides a UUID primary key and timestamp fields.
    Inherits from Timestampable to include `created_at` and `updated_at` fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,name='id')

    class Meta:
        abstract = True
