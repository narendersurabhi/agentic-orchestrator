import json

from runtime.common import (
    Settings,
    configure_logging,
    create_consumer,
    create_producer,
    get_logger,
)

logger = get_logger(__name__)


def handle_event(event: dict) -> None:
    if event.get("type") == "ToolCompleted":
        task_id = event.get("payload", {}).get("task_id")
        logger.info("Resuming task", extra={"task_id": task_id})


def run() -> None:
    settings = Settings.from_env()
    settings.validate()
    configure_logging(settings.service_name, settings.log_level)

    consumer = create_consumer(settings, "result-router", ["tool.events"])
    producer = create_producer(settings)

    logger.info("Result router started")
    try:
        while True:
            msg = consumer.poll(0.2)
            if not msg:
                continue
            if msg.error():
                logger.error("Kafka error: %s", msg.error())
                continue
            payload = msg.value()
            if payload is None:
                logger.warning("Received empty message payload")
                continue
            event = json.loads(payload)
            handle_event(event)
            consumer.commit(msg)
    except KeyboardInterrupt:
        logger.info("Result router shutting down")
    finally:
        producer.flush(5)
        consumer.close()


if __name__ == "__main__":
    run()
