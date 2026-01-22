from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    kafka_bootstrap: str
    kafka_security_protocol: str
    kafka_sasl_mechanism: str
    kafka_sasl_username: str
    kafka_sasl_password: str
    log_level: str
    service_name: str

    @classmethod
    def from_env(
        cls, environ: Mapping[str, str] | None = None, load_env: bool = True
    ) -> "Settings":
        if load_env:
            load_dotenv()
        env = environ or os.environ
        return cls(
            kafka_bootstrap=env.get("KAFKA_BOOTSTRAP", ""),
            kafka_security_protocol=env.get("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),
            kafka_sasl_mechanism=env.get("KAFKA_SASL_MECHANISM", "PLAIN"),
            kafka_sasl_username=env.get("KAFKA_SASL_USERNAME", ""),
            kafka_sasl_password=env.get("KAFKA_SASL_PASSWORD", ""),
            log_level=env.get("LOG_LEVEL", "INFO"),
            service_name=env.get("SERVICE_NAME", "agentic-orchestrator"),
        )

    def validate(self) -> None:
        missing = [
            name
            for name, value in (
                ("KAFKA_BOOTSTRAP", self.kafka_bootstrap),
                ("KAFKA_SASL_USERNAME", self.kafka_sasl_username),
                ("KAFKA_SASL_PASSWORD", self.kafka_sasl_password),
            )
            if not value
        ]
        if missing:
            missing_list = ", ".join(missing)
            raise ValueError(f"Missing required environment variables: {missing_list}")

    def kafka_security(self) -> dict[str, str]:
        return {
            "bootstrap.servers": self.kafka_bootstrap,
            "security.protocol": self.kafka_security_protocol,
            "sasl.mechanisms": self.kafka_sasl_mechanism,
            "sasl.username": self.kafka_sasl_username,
            "sasl.password": self.kafka_sasl_password,
        }
