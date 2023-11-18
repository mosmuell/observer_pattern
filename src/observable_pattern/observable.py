import logging
from typing import Any

from observable_pattern.observable_object import ObservableObject

logger = logging.getLogger(__name__)


class Observable(ObservableObject):
    def __init__(self) -> None:
        super().__init__()
        class_attrs = {
            k: type(self).__dict__[k]
            for k in set(type(self).__dict__)
            - set(Observable.__dict__)
            - set(self.__dict__)
        }
        for name, value in class_attrs.items():
            self.__dict__[name] = self._initialise_new_objects(name, value)

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, "_observers"):
            self._remove_observer_if_observable(name)
            value = self._initialise_new_objects(name, value)
            self._notify_observers(name, value)

        super().__setattr__(name, value)

    def _notify_observers(self, changed_attribute: Any, value: Any) -> None:
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                extendend_attr_path = changed_attribute
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}.{changed_attribute}"
                observer._notify_observers(extendend_attr_path, value)

    def _remove_observer_if_observable(self, name: Any) -> None:
        current_value = getattr(self, name, None)

        if isinstance(current_value, ObservableObject):
            current_value._remove_observer(self, name)
