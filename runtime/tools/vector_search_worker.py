import json
import time

from runtime.common import (
    Settings,
    configure_logging,
    create_consumer,
    create_producer,
    get_logger,
)

logger = get_logger(__name__)


def handle_event(event: dict, producer) -> None:
    if (
        event.get("type") == "ToolRequested"
        and event.get("payload", {}).get("tool") == "vector_search"
    ):
        time.sleep(0.5)
        out = {
            "version": "1",
            "type": "ToolCompleted",
            "event_id": f"{event['event_id']}c",
            "occurred_at": event["occurred_at"],
            "tenant_id": event["tenant_id"],
            "plan_id": event["plan_id"],
            "payload": {
                "task_id": event["payload"]["task_id"],
                "tool_call_id": event["payload"]["tool_call_id"],
                "outputs_ref": "s3://outputs/vs_out.json",
                "metrics": {"lat_ms": 500},
            },
        }
        producer.produce(
            "tool.events", key=event["plan_id"], value=json.dumps(out).encode("utf-8")
        )
        producer.flush()
        logger.info("Tool completed", extra={"task_id": event["payload"]["task_id"]})


def run() -> None:
    settings = Settings.from_env()
    settings.validate()
    configure_logging(settings.service_name, settings.log_level)

    consumer = create_consumer(settings, "tools.vector_search", ["tool.events"])
    producer = create_producer(settings)

    logger.info("Vector search worker started")
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
            handle_event(event, producer)
            consumer.commit(msg)
    except KeyboardInterrupt:
        logger.info("Vector search worker shutting down")
    finally:
        producer.flush(5)
        consumer.close()


if __name__ == "__main__":
    run()
