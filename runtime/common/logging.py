import logging
from typing import TextIO


class ServiceFilter(logging.Filter):
    def __init__(self, service_name: str) -> None:
        super().__init__()
        self.service_name = service_name

    def filter(self, record: logging.LogRecord) -> bool:
        record.service_name = self.service_name
        return True


def configure_logging(
    service_name: str, log_level: str, stream: TextIO | None = None
) -> None:
    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(service_name)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)
    handler.addFilter(ServiceFilter(service_name))

    root = logging.getLogger()
    root.setLevel(log_level.upper())
    root.handlers.clear()
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
