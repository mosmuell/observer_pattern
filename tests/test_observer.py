import observable_pattern.observer
import pytest


def test_abstract_method_error() -> None:
    class MyObserver(observable_pattern.observer.Observer):
        pass

    with pytest.raises(TypeError):
        MyObserver()
