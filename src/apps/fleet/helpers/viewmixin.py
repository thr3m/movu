from django.core.exceptions import ImproperlyConfigured


class MultiSerializerViewSetMixin:
    """
    Mixin to allow a ViewSet to use different serializers for different actions.
    """

    serializers = {"default": None}

    def get_serializer_class(self):
        """
        Return the serializer class to use based on the action.

        Defaults to the 'default' serializer if action-specific serializer is not found.
        Raises ImproperlyConfigured if 'serializers' attribute is missing.
        """
        if not hasattr(self, "serializer_class"):
            raise ImproperlyConfigured(
                "%(cls)s is missing a 'serializers' attribute. Define "
                "%(cls)s.serializers dictionary or override "
                "%(cls)s.get_serializer_class(). " % {"cls": self.__class__.__name__}
            )

        return self.serializers.get(self.action, self.serializers.get("default"))
