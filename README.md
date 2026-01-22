# agentic-orchestrator
Streaming-first, event-sourced multi-agent orchestration on **Confluent Cloud**. Public repo. MIT license.

## Stack
- Backbone: Confluent Cloud Kafka. Schema Registry for all events.
- State: DynamoDB. Artifacts: S3. Guardrails: Flink (optional).
- Services: PlanCoordinator, ResultRouter, Agent and Tool workers.
- UI: React DAG status page.

## Configure
Copy `.env.example` to `.env` and set Confluent Cloud and AWS variables.

### Observability
- `LOG_LEVEL` controls runtime log verbosity (default: `INFO`).
- `SERVICE_NAME` labels log output for multi-service deployments.

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r runtime/requirements.txt
npm --prefix ui ci
npm --prefix ui run build
```

## Run locally
```bash
# load .env
export $(grep -v '^#' .env | xargs -d '\n' -I {} echo {})

# start consumers/producers
python runtime/coordinators/plan_coordinator.py
python runtime/coordinators/result_router.py
python runtime/agents/planner.py
python runtime/tools/vector_search_worker.py
```

## Tests
```bash
pip install -r runtime/requirements-dev.txt
pytest
```
