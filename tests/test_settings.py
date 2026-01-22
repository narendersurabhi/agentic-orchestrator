import pytest

from runtime.common.settings import Settings


def test_settings_validate_missing_required() -> None:
    settings = Settings(
        kafka_bootstrap="",
        kafka_security_protocol="SASL_SSL",
        kafka_sasl_mechanism="PLAIN",
        kafka_sasl_username="",
        kafka_sasl_password="",
        log_level="INFO",
        service_name="test",
    )
    with pytest.raises(ValueError) as excinfo:
        settings.validate()
    assert "KAFKA_BOOTSTRAP" in str(excinfo.value)


def test_settings_validate_success() -> None:
    settings = Settings(
        kafka_bootstrap="localhost:9092",
        kafka_security_protocol="SASL_SSL",
        kafka_sasl_mechanism="PLAIN",
        kafka_sasl_username="user",
        kafka_sasl_password="pass",
        log_level="INFO",
        service_name="test",
    )
    settings.validate()
