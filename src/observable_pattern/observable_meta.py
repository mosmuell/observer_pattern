import logging
from typing import cast

from observable_pattern.observable_object import ObservableObject

logger = logging.getLogger(__name__)


class ObservableMeta:
    def __new__(cls):  # type: ignore[no-untyped-def]
        instance = super().__new__(cls)
        attrs = dict(cls.__dict__.items())
        for name, value in attrs.items():
            instance.__dict__[name] = cast(
                ObservableObject, instance
            ).initialise_new_objects(name, value)
        return instance
