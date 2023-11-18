from typing import Any

import observable_pattern.observer
import pytest
from observable_pattern.observable import Observable


def test_abstract_method_error() -> None:
    class MyObserver(observable_pattern.observer.Observer):
        pass

    class MyObservable(Observable):
        pass

    with pytest.raises(TypeError):
        MyObserver(MyObservable())


def test_constructor_error() -> None:
    class MyObserver(observable_pattern.observer.Observer):
        def on_change(self, full_access_path: str, value: Any) -> None:
            pass

    with pytest.raises(TypeError):
        MyObserver()
