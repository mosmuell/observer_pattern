import logging

from observable_pattern.observable import Observable
from observable_pattern.utils.logging import setup_logging

setup_logging(logging.DEBUG)

__all__ = ["Observable"]
