import logging
from typing import Any

import observable_pattern
import observable_pattern.observable_object
import pytest
from observable_pattern.observer import Observer

logger = logging.getLogger(__name__)


class MyObserver(Observer):
    def on_change(self, full_access_path: str, value: Any) -> None:
        logger.info("'%s' changed to '%s'", full_access_path, value)


def test_simple_class_attribute(caplog: pytest.LogCaptureFixture) -> None:
    class MyObservable(observable_pattern.Observable):
        int_attribute = 10

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.int_attribute = 12

    assert "'int_attribute' changed to '12'" in caplog.text  # noqa: S101


def test_simple_instance_attribute(caplog: pytest.LogCaptureFixture) -> None:
    class MyObservable(observable_pattern.Observable):
        def __init__(self) -> None:
            super().__init__()
            self.int_attribute = 10

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.int_attribute = 12

    assert "'int_attribute' changed to '12'" in caplog.text  # noqa: S101


def test_nested_class_attribute(caplog: pytest.LogCaptureFixture) -> None:
    class MySubclass(observable_pattern.Observable):
        name = "My Subclass"

    class MyObservable(observable_pattern.Observable):
        subclass = MySubclass()

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.subclass.name = "Other name"

    assert "'subclass.name' changed to 'Other name'" in caplog.text  # noqa: S101


def test_nested_instance_attribute(caplog: pytest.LogCaptureFixture) -> None:
    class MySubclass(observable_pattern.Observable):
        def __init__(self) -> None:
            super().__init__()
            self.name = "Subclass name"

    class MyObservable(observable_pattern.Observable):
        def __init__(self) -> None:
            super().__init__()
            self.subclass = MySubclass()

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.subclass.name = "Other name"

    assert "'subclass.name' changed to 'Other name'" in caplog.text  # noqa: S101


def test_removed_observer_on_class_attr(caplog: pytest.LogCaptureFixture) -> None:
    class NestedObservable(observable_pattern.Observable):
        name = "Hello"

    nested_instance = NestedObservable()

    class MyObservable(observable_pattern.Observable):
        nested_attr = nested_instance
        changed_attr = nested_instance

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.changed_attr = "Ciao"

    assert "'changed_attr' changed to 'Ciao'" in caplog.text  # noqa: S101
    caplog.clear()

    instance.nested_attr.name = "Hi"

    assert "'nested_attr.name' changed to 'Hi'" in caplog.text
    assert "'changed_attr.name' changed to 'Hi'" not in caplog.text


def test_removed_observer_on_instance_attr(caplog: pytest.LogCaptureFixture) -> None:
    class NestedObservable(observable_pattern.Observable):
        def __init__(self) -> None:
            super().__init__()
            self.name = "Hello"

    nested_instance = NestedObservable()

    class MyObservable(observable_pattern.Observable):
        def __init__(self) -> None:
            super().__init__()
            self.nested_attr = nested_instance
            self.changed_attr = nested_instance

    instance = MyObservable()
    instance.add_observer(MyObserver())
    instance.changed_attr = "Ciao"

    assert "'changed_attr' changed to 'Ciao'" in caplog.text  # noqa: S101
    caplog.clear()

    instance.nested_attr.name = "Hi"

    assert "'nested_attr.name' changed to 'Hi'" in caplog.text
    assert "'changed_attr.name' changed to 'Hi'" not in caplog.text
