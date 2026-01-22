from __future__ import annotations

from typing import Sequence

from confluent_kafka import Consumer, Producer

from .settings import Settings

KafkaConsumerConfigValue = str | int | float | bool | None
KafkaProducerConfigValue = str | int | float | bool


def kafka_consumer_config(
    settings: Settings, group_id: str, auto_offset_reset: str = "earliest"
) -> dict[str, KafkaConsumerConfigValue]:
    config: dict[str, KafkaConsumerConfigValue] = dict(settings.kafka_security())
    config.update(
        {
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset,
        }
    )
    return config


def kafka_producer_config(settings: Settings) -> dict[str, KafkaProducerConfigValue]:
    return dict(settings.kafka_security())


def create_consumer(
    settings: Settings, group_id: str, topics: Sequence[str]
) -> Consumer:
    consumer = Consumer(kafka_consumer_config(settings, group_id))
    consumer.subscribe(list(topics))
    return consumer


def create_producer(settings: Settings) -> Producer:
    return Producer(kafka_producer_config(settings))
