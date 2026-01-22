# Minimal placeholder for Schema Registry registration
import glob
import os

import requests  # type: ignore[import-untyped]

SR_URL = os.environ.get("SCHEMA_REGISTRY_URL")
SR_KEY = os.environ.get("SCHEMA_REGISTRY_API_KEY")
SR_SECRET = os.environ.get("SCHEMA_REGISTRY_API_SECRET")
if not SR_URL:
    print("SCHEMA_REGISTRY_URL not set; skipping")
    raise SystemExit(0)
headers = {"Content-Type": "application/vnd.schemaregistry.v1+json"}
auth = (SR_KEY, SR_SECRET) if SR_KEY and SR_SECRET else None
for path in glob.glob("runtime/schemas/*.schema.json"):
    subject = os.path.basename(path).replace(".schema.json", "")
    with open(path) as schema_file:
        data = {"schemaType": "JSON", "schema": schema_file.read()}
    r = requests.post(
        f"{SR_URL}/subjects/{subject}/versions", json=data, headers=headers, auth=auth
    )
    print(subject, r.status_code, r.text[:200])
