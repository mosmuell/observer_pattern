import logging
from typing import Any

from observable_pattern.observable_meta import ObservableMeta
from observable_pattern.observable_object import ObservableObject

logger = logging.getLogger(__name__)


class Observable(ObservableObject, ObservableMeta):
    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, "_observers"):
            self.remove_observer_if_observable(name)
            value = self.initialise_new_objects(name, value)
            self.notify_observers(name, value)

        super().__setattr__(name, value)
