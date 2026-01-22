from runtime.common import get_logger

logger = get_logger(__name__)


def report(event) -> None:
    logger.info("Agent event", extra={"event": event})
