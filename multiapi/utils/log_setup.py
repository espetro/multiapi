import logging
import os


def setup_logging():
    """
    Logging level can be set up via the environment variable 'LOG_LEVEL'. The available log levels are listed in
    https://docs.python.org/3/library/logging.html#logging-levels
    """
    logging.basicConfig(
        level=_get_log_level(),
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def _get_log_level() -> int:
    raw_level = os.getenv("LOG_LEVEL", "INFO")
    log_level = logging.getLevelName(raw_level)

    return logging.INFO if not isinstance(log_level, int) else log_level
