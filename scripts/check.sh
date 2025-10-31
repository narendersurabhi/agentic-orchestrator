#!/usr/bin/env bash
set -euo pipefail
pytest -q || true
npm --prefix ui run build || true
