import logging
from typing import Any, cast

from observable_pattern.observable_object import ObservableObject

logger = logging.getLogger(__name__)


def get_instance_unique_dict(instance: Any) -> dict[str, Any]:
    unique_attrs = {}
    base_attrs = {
        attr for cls in [ObservableObject, ObservableMeta] for attr in cls.__dict__
    }
    logger.debug(base_attrs)

    for attr, value in instance.__dict__.items():
        if attr not in base_attrs:
            unique_attrs[attr] = value

    return unique_attrs


class ObservableMeta:
    def __new__(cls):  # type: ignore[no-untyped-def]
        instance = super().__new__(cls)
        instance_attrs = {
            key: value
            for key, value in instance.__dict__.items()
            if not key.startswith("_")
        }
        # logger.debug(instance_attrs)

        for name, value in instance_attrs.items():
            instance.__dict__[name] = cast(
                ObservableObject, instance
            ).initialise_new_objects(name, value)
        return instance
