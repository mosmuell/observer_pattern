import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from observer_pattern.observer.observer import Observer

logger = logging.getLogger(__name__)


class ObservableObject(ABC):
    _list_mapping: ClassVar[dict[int, "_ObservableList"]] = {}
    _dict_mapping: ClassVar[dict[int, "_ObservableDict"]] = {}

    def __init__(self) -> None:
        self._observers: dict[str | None, list["ObservableObject | Observer"]] = {}

    def add_observer(
        self, observer: "ObservableObject | Observer", attr_name: str = ""
    ) -> None:
        if attr_name not in self._observers:
            self._observers[attr_name] = []
        if observer not in self._observers[attr_name]:
            self._observers[attr_name].append(observer)

    def _remove_observer(self, observer: "ObservableObject", attribute: str) -> None:
        if attribute in self._observers:
            self._observers[attribute].remove(observer)

    @abstractmethod
    def _remove_observer_if_observable(self, name: str) -> None:
        ...

    @abstractmethod
    def _notify_observers(self, changed_attribute: str, value: Any) -> None:
        ...

    def _initialise_new_objects(self, attr_name_or_key: Any, value: Any) -> Any:
        new_value = value
        if isinstance(value, list):
            if id(value) in self._list_mapping:
                # If the list `value` was already referenced somewhere else
                new_value = self._list_mapping[id(value)]
            else:
                # convert the builtin list into a ObservableList
                new_value = _ObservableList(original_list=value)
                self._list_mapping[id(value)] = new_value
        elif isinstance(value, dict):
            if id(value) in self._dict_mapping:
                # If the list `value` was already referenced somewhere else
                new_value = self._dict_mapping[id(value)]
            else:
                # convert the builtin list into a ObservableList
                new_value = _ObservableDict(original_dict=value)
                self._dict_mapping[id(value)] = new_value
        if isinstance(new_value, ObservableObject):
            new_value.add_observer(self, str(attr_name_or_key))
        return new_value


class _ObservableList(ObservableObject, list):
    def __init__(
        self,
        original_list: list[Any],
    ) -> None:
        self._original_list = original_list
        ObservableObject.__init__(self)
        list.__init__(self, self._original_list)
        for i, item in enumerate(self._original_list):
            super().__setitem__(i, self._initialise_new_objects(f"[{i}]", item))

    def __setitem__(self, key: int, value: Any) -> None:  # type: ignore[override]
        if hasattr(self, "_observers"):
            self._remove_observer_if_observable(f"[{key}]")
            value = self._initialise_new_objects(f"[{key}]", value)
            self._notify_observers(f"[{key}]", value)

        super().__setitem__(key, value)

    def _notify_observers(self, changed_attribute: str, value: Any) -> None:
        changed_attribute = str(changed_attribute)
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                extendend_attr_path = changed_attribute
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}{extendend_attr_path}"
                observer._notify_observers(extendend_attr_path, value)

    def _remove_observer_if_observable(self, name: str) -> None:
        key = int(name[1:-1])
        current_value = self.__getitem__(key)

        if isinstance(current_value, ObservableObject):
            current_value._remove_observer(self, name)


# TODO(mosmuell): keys must be strings.. Maybe with a metaclass?
class _ObservableDict(dict, ObservableObject):
    def __init__(
        self,
        original_dict: dict[Any, Any],
    ) -> None:
        self._original_dict = original_dict
        ObservableObject.__init__(self)
        dict.__init__(self)
        for key, value in self._original_dict.items():
            super().__setitem__(key, self._initialise_new_objects(f"['{key}']", value))

    def __setitem__(self, key: str, value: Any) -> None:  # type: ignore[override]
        if not isinstance(key, str):
            logger.warning(
                "Dictionary key %s is not a string. Trying to convert to string...", key
            )
            key = str(key)

        if hasattr(self, "_observers"):
            self._remove_observer_if_observable(f"['{key}']")
            value = self._initialise_new_objects(key, value)
            self._notify_observers(f"['{key}']", value)

        super().__setitem__(key, value)

    def _notify_observers(self, changed_attribute: str, value: Any) -> None:
        changed_attribute = str(changed_attribute)
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                extendend_attr_path = changed_attribute
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}{extendend_attr_path}"
                observer._notify_observers(extendend_attr_path, value)

    def _remove_observer_if_observable(self, name: str) -> None:
        key = name[2:-2]
        current_value = self.get(key, None)

        if isinstance(current_value, ObservableObject):
            current_value._remove_observer(self, name)