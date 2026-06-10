"""Logging configuration for the Grand Line Character Builder.

Sets up structured logging with two handlers:
- Console handler at INFO level for runtime visibility.
- File handler at DEBUG level for detailed debugging in rpg_app.log.
"""

import logging
import sys


def setup_logging() -> None:
    """Configure the root logger with console and file handlers.

    Sets the root logger to DEBUG level so all messages are captured.
    The console handler filters to INFO and above to avoid noise in
    the terminal, while the file handler captures everything from
    DEBUG upwards for detailed troubleshooting.

    The log format includes timestamp, level, logger name, and message.
    Logs are written to rpg_app.log in the project root directory.
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if root_logger.handlers:
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("rpg_app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)