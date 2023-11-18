from typing import Any

import observer_pattern.observer
import pytest
from observer_pattern.observable import Observable


def test_abstract_method_error() -> None:
    class MyObserver(observer_pattern.observer.Observer):
        pass

    class MyObservable(Observable):
        pass

    with pytest.raises(TypeError):
        MyObserver(MyObservable())


def test_constructor_error() -> None:
    class MyObserver(observer_pattern.observer.Observer):
        def on_change(self, full_access_path: str, value: Any) -> None:
            pass

    with pytest.raises(TypeError):
        MyObserver()
