import logging
import sys
from collections.abc import Callable
from copy import copy
from typing import ClassVar, Literal, Optional

import click


class ColourizedFormatter(logging.Formatter):
    """
    A custom log formatter class that:

    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extras={"color_message": ...}` it will be used
      for formatting the output, instead of the plain text message.
    """

    level_name_colors: ClassVar[dict[int, Callable[..., str]]] = {
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red"
        ),
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        use_colors: Optional[bool] = None,
    ) -> None:
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        def default(level_name: str) -> str:
            return str(level_name)  # pragma: no cover

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def formatMessage(self, record: logging.LogRecord) -> str:  # noqa: N802
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()
        recordcopy.__dict__["levelprefix"] = levelname + seperator
        return logging.Formatter.formatMessage(self, recordcopy)

    def should_use_colors(self) -> bool:
        return sys.stderr.isatty()  # pragma: no cover


def setup_logging(level: str | int = logging.INFO) -> None:
    """
    Configures the logging settings for the application.

    This function sets up logging with specific formatting and colorization of log
    messages. The log level is determined based on the application's operation mode,
    with an option to override the level. By default, in a development environment, the
    log level is set to DEBUG, whereas in other environments, it is set to INFO.

    Args:
        level (Optional[str | int]):
            A specific log level to set for the application. If None, the log level is
            determined based on the application's operation mode. Accepts standard log
            level names ('DEBUG', 'INFO', etc.) and corresponding numerical values.

    Example:

    ```python
    >>> import logging
    >>> setup_logging(logging.DEBUG)
    >>> setup_logging("INFO")
    ```
    """

    logger = logging.getLogger()

    if isinstance(level, str):
        # Convert known log level strings directly to their corresponding logging
        # module constants.
        level_name = level.upper()  # Ensure level names are uppercase
        if hasattr(logging, level_name):
            log_level = getattr(logging, level_name)
        else:
            raise ValueError(
                f"Invalid log level: {level}. Must be one of 'DEBUG', 'INFO', "
                "'WARNING', 'ERROR', etc."
            )
    elif isinstance(level, int):
        log_level = level  # Directly use integer levels
    else:
        raise ValueError("Log level must be a string or an integer.")

    # Set the logger's level.
    logger.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()

    # add formatter to ch
    ch.setFormatter(
        ColourizedFormatter(
            fmt="%(asctime)s.%(msecs)03d | %(levelprefix)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # add ch to logger
    logger.addHandler(ch)

    logger.debug("Configuring service logging.")
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)
