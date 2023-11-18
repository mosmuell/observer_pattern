import logging
from typing import Any

import observable_pattern
from observable_pattern.observer import Observer

logger = logging.getLogger(__name__)


class MyObserver(Observer):
    def on_change(self, full_access_path: str, value: Any) -> None:
        logger.info("'%s' changed to '%s'", full_access_path, value)


class MySubclass(observable_pattern.Observable):
    name = "My Subclass"


class MyObservable(observable_pattern.Observable):
    subclass = MySubclass()


instance = MyObservable()
instance.add_observer(MyObserver())
instance.subclass.name = "Other name"
