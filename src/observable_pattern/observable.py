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
            logger.debug("Initialising %s", name)
            self.__dict__[name] = self.initialise_new_objects(name, value)

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, "_observers"):
            self.remove_observer_if_observable(name)
            value = self.initialise_new_objects(name, value)
            self.notify_observers(name, value)

        super().__setattr__(name, value)
