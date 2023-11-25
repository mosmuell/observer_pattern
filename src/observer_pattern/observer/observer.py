from abc import ABC, abstractmethod
from typing import Any

from observer_pattern.observable import Observable


class Observer(ABC):
    def __init__(self, observable: Observable) -> None:
        self.observable = observable
        self.observable.add_observer(self)

    def _notify_changed(self, changed_attribute: str, value: Any) -> None:
        self.on_change(full_access_path=changed_attribute, value=value)

    @abstractmethod
    def on_change(self, full_access_path: str, value: Any) -> None:
        ...
