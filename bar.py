import logging
from enum import Enum
from typing import Any

import observable_pattern
import observable_pattern.observable_object
from observable_pattern.observer import Observer

logger = logging.getLogger(__name__)


class SomeEnum(Enum):
    STATE = "hi"


class MyObserver(Observer):
    def on_change(self, full_access_path: str, value: Any) -> None:
        logger.info("'%s' changed to '%s'", full_access_path, value)


class MyObservable(observable_pattern.Observable):
    def __init__(self) -> None:
        super().__init__()
        self.dict_attr = {SomeEnum.STATE: "Hi", "SomeEnum.STATE": "Hello"}


instance = MyObservable()
instance.add_observer(MyObserver())
for key, value in instance.dict_attr.items():
    print(f"[{key}]", value)
