import os, json
from confluent_kafka import Consumer, Producer
from fastjsonschema import compile as jc
from dotenv import load_dotenv
load_dotenv()
ENV = os.environ.get

def consumer_cfg(group):
    return {
        'bootstrap.servers': ENV('KAFKA_BOOTSTRAP'),
        'group.id': group,
        'security.protocol': ENV('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
        'sasl.mechanisms': ENV('KAFKA_SASL_MECHANISM','PLAIN'),
        'sasl.username': ENV('KAFKA_SASL_USERNAME'),
        'sasl.password': ENV('KAFKA_SASL_PASSWORD'),
        'auto.offset.reset': 'earliest'
    }

consumer = Consumer(consumer_cfg('plan-coordinator'))
producer = Producer({'bootstrap.servers': ENV('KAFKA_BOOTSTRAP'),
                     'security.protocol': ENV('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
                     'sasl.mechanisms': ENV('KAFKA_SASL_MECHANISM','PLAIN'),
                     'sasl.username': ENV('KAFKA_SASL_USERNAME'),
                     'sasl.password': ENV('KAFKA_SASL_PASSWORD')})

consumer.subscribe(['plan.events','task.events','tool.events'])

while True:
    msg = consumer.poll(0.2)
    if not msg: 
        continue
    if msg.error():
        continue
    evt = json.loads(msg.value())
    # TODO: readiness math + writes to PlanStore/TaskStore/ToolReqStore
    # For now, just echo for visibility
    print('[plan-coordinator]', evt.get('type'))
    consumer.commit(msg)
