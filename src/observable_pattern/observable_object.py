import logging
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


class ObservableObject:
    _list_mapping: ClassVar[dict[int, "_ObservableList"]] = {}
    _dict_mapping: ClassVar[dict[int, "_ObservableDict"]] = {}

    def __init__(self) -> None:
        # TODO(mosmuell): Implement an "initialised" attribute. I don't want to convert
        # the _observers into a _ObservableDict
        self._observers: dict[str | None, list["ObservableObject"]] = {}

    def add_observer(
        self, observer: "ObservableObject", attr_or_item: str = ""
    ) -> None:
        if attr_or_item not in self._observers:
            self._observers[attr_or_item] = []
        if observer not in self._observers[attr_or_item]:
            self._observers[attr_or_item].append(observer)

    def remove_observer(self, observer: "ObservableObject", attribute: str) -> None:
        if attribute in self._observers:
            self._observers[attribute].remove(observer)

    def remove_observer_if_observable(self, name: Any) -> None:
        current_value = getattr(self, name, None)

        if isinstance(current_value, ObservableObject):
            current_value.remove_observer(self, name)

    def notify_observers(self, changed_attribute: Any, value: Any) -> None:
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                extendend_attr_path = changed_attribute
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}.{changed_attribute}"
                observer.notify_observers(extendend_attr_path, value)

    def initialise_new_objects(self, attr_name_or_key: Any, value: Any) -> Any:
        if isinstance(value, list):
            if id(value) in self._list_mapping:
                # If the list `value` was already referenced somewhere else
                value = self._list_mapping[id(value)]
            else:
                # convert the builtin list into a ObservableList
                value = _ObservableList(original_list=value)
                self._list_mapping[id(value)] = value
        elif isinstance(value, dict):
            if id(value) in self._dict_mapping:
                # If the list `value` was already referenced somewhere else
                value = self._dict_mapping[id(value)]
            else:
                # convert the builtin list into a ObservableList
                value = _ObservableDict(original_dict=value)
                self._dict_mapping[id(value)] = value
        if isinstance(value, ObservableObject):
            value.add_observer(self, str(attr_name_or_key))
        return value


class _ObservableList(list, ObservableObject):
    def __init__(
        self,
        original_list: list[Any],
    ) -> None:
        self._original_list = original_list
        ObservableObject.__init__(self)
        list.__init__(self, self._original_list)
        for i, item in enumerate(self._original_list):
            self[i] = self.initialise_new_objects(i, item)

    def __setitem__(self, key: int, value: Any) -> None:  # type: ignore[override]
        if hasattr(self, "_observers"):
            self.remove_observer_if_observable(key)
            value = self.initialise_new_objects(key, value)
            self.notify_observers(key, value)

        super().__setitem__(key, value)

    def notify_observers(self, changed_attribute: Any, value: Any) -> None:
        changed_attribute = str(changed_attribute)
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                key, rest = (
                    changed_attribute.split(".")[0],
                    changed_attribute.split(".")[1:],
                )
                extendend_attr_path = ".".join([f"[{key}]", *rest])
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}{extendend_attr_path}"
                observer.notify_observers(extendend_attr_path, value)

    def remove_observer_if_observable(self, name: Any) -> None:
        current_value = self.__getitem__(name)

        if isinstance(current_value, ObservableObject):
            current_value.remove_observer(self, str(name))


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
            self[key] = self.initialise_new_objects(key, value)

    def __setitem__(self, key: Any, value: Any) -> None:  # type: ignore[override]
        if not isinstance(key, str):
            logger.warning(
                "Dictionary key %s is not a string. Trying to convert to string...", key
            )
            key = str(key)

        if hasattr(self, "_observers"):
            self.remove_observer_if_observable(key)
            value = self.initialise_new_objects(key, value)
            self.notify_observers(key, value)

        super().__setitem__(key, value)

    def notify_observers(self, changed_attribute: Any, value: Any) -> None:
        changed_attribute = str(changed_attribute)
        for attr_name, observer_list in self._observers.items():
            for observer in observer_list:
                key, rest = (
                    changed_attribute.split(".")[0],
                    changed_attribute.split(".")[1:],
                )
                extendend_attr_path = ".".join([f"[{key}]", *rest])
                if attr_name != "":
                    extendend_attr_path = f"{attr_name}{extendend_attr_path}"
                observer.notify_observers(extendend_attr_path, value)

    def remove_observer_if_observable(self, name: str) -> None:
        current_value = self.get(name, None)

        if isinstance(current_value, ObservableObject):
            current_value.remove_observer(self, name)
