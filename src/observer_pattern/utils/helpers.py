from typing import Any


def is_property_attribute(target_obj: Any, attr_name: str) -> bool:
    return isinstance(getattr(type(target_obj), attr_name, None), property)
