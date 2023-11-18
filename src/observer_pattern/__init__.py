import logging

from observer_pattern.observable import Observable
from observer_pattern.observer import Observer
from observer_pattern.utils.logging import setup_logging

setup_logging(logging.DEBUG)

__all__ = [
    "Observable",
    "Observer",
]
