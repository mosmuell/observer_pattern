from abc import abstractmethod
from typing import Any

from observable_pattern.observable_object import ObservableObject


class Observer(ObservableObject):
    def _notify_observers(self, changed_attribute: str, value: Any) -> None:
        self.on_change(full_access_path=changed_attribute, value=value)

    def _remove_observer_if_observable(self, name: Any) -> None:
        pass

    @abstractmethod
    def on_change(self, full_access_path: str, value: Any) -> None:
        ...
