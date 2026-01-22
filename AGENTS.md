# AGENTS

This file tracks repository changes for maintainers and future agents.

## Current Status
- Observability and configuration have been centralized in `runtime/common`.
- Core runtime scripts use structured logging and validated settings.
- Basic pytest coverage exists for settings validation.

## Change Log
- 2026-01-22: Added shared settings/logging/kafka helpers, refactored runtime workers to use them, added tests and dev requirements, and expanded environment examples for log configuration.
- 2026-01-22: Cleaned up schema registry script imports and file handling per linting requirements.
- 2026-01-22: Addressed type-checking findings with Kafka config typing, logging stream types, and safer Kafka message handling.
- 2026-01-22: Added pytest configuration to ensure repository imports resolve during tests.
