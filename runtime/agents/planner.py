import json
import time
import uuid

from runtime.common import Settings, configure_logging, create_producer, get_logger

logger = get_logger(__name__)


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def emit(producer, topic: str, key: str, event: dict) -> None:
    producer.produce(topic, key=key, value=json.dumps(event).encode("utf-8"))
    producer.flush()


def run() -> None:
    settings = Settings.from_env()
    settings.validate()
    configure_logging(settings.service_name, settings.log_level)

    producer = create_producer(settings)
    plan_id = f"plan_{uuid.uuid4().hex[:8]}"

    plan_created = {
        "version": "1",
        "type": "PlanCreated",
        "event_id": uuid.uuid4().hex,
        "occurred_at": now(),
        "tenant_id": "t_demo",
        "plan_id": plan_id,
        "payload": {
            "graph": {
                "nodes": [
                    {
                        "id": "t_retrieve",
                        "kind": "task",
                        "type": "retrieve",
                        "deps": [],
                    },
                    {
                        "id": "tc_vs_1",
                        "kind": "tool",
                        "tool": "vector_search",
                        "deps": ["t_retrieve"],
                    },
                    {
                        "id": "t_draft",
                        "kind": "task",
                        "type": "draft",
                        "deps": ["tc_vs_1"],
                    },
                    {
                        "id": "t_finish",
                        "kind": "task",
                        "type": "aggregate",
                        "deps": ["t_draft"],
                    },
                ],
                "edges": [
                    ["t_retrieve", "tc_vs_1"],
                    ["tc_vs_1", "t_draft"],
                    ["t_draft", "t_finish"],
                ],
            },
            "constraints": {"max_depth": 4, "max_width": 12, "budget_tokens": 120000},
        },
    }
    emit(producer, "plan.events", plan_id, plan_created)

    emit(
        producer,
        "task.events",
        plan_id,
        {
            "version": "1",
            "type": "TaskCreated",
            "event_id": uuid.uuid4().hex,
            "occurred_at": now(),
            "tenant_id": "t_demo",
            "plan_id": plan_id,
            "payload": {
                "task_id": "t_retrieve",
                "type": "retrieve",
                "inputs_ref": "s3://inputs/retrieve.json",
                "deps": [],
            },
        },
    )

    emit(
        producer,
        "tool.events",
        plan_id,
        {
            "version": "1",
            "type": "ToolRequested",
            "event_id": uuid.uuid4().hex,
            "occurred_at": now(),
            "tenant_id": "t_demo",
            "plan_id": plan_id,
            "payload": {
                "task_id": "t_draft",
                "tool_call_id": "tc_vs_1",
                "tool": "vector_search",
                "inputs_ref": "s3://inputs/vs.json",
                "deps": ["t_retrieve"],
                "continuation": "cont_demo",
            },
        },
    )

    logger.info("Seed plan emitted", extra={"plan_id": plan_id})


if __name__ == "__main__":
    run()
