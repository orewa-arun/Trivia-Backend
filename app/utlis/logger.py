import inspect
import logging
import sys


def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_with_method(logger: logging.Logger, level: str, message: str):
    frame = inspect.currentframe()
    method = frame.f_back.f_code.co_name if frame and frame.f_back else "<unknown>"
    full_message = f"[{method}] {message}"
    getattr(logger, level)(full_message)