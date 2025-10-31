import os, json
from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv
load_dotenv()
ENV = os.environ.get
consumer = Consumer({
    'bootstrap.servers': ENV('KAFKA_BOOTSTRAP'),
    'group.id': 'result-router',
    'security.protocol': ENV('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
    'sasl.mechanisms': ENV('KAFKA_SASL_MECHANISM','PLAIN'),
    'sasl.username': ENV('KAFKA_SASL_USERNAME'),
    'sasl.password': ENV('KAFKA_SASL_PASSWORD'),
    'auto.offset.reset': 'earliest'
})
producer = Producer({'bootstrap.servers': ENV('KAFKA_BOOTSTRAP'),
                     'security.protocol': ENV('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
                     'sasl.mechanisms': ENV('KAFKA_SASL_MECHANISM','PLAIN'),
                     'sasl.username': ENV('KAFKA_SASL_USERNAME'),
                     'sasl.password': ENV('KAFKA_SASL_PASSWORD')})
consumer.subscribe(['tool.events'])
while True:
    m = consumer.poll(0.2)
    if not m: continue
    if m.error(): continue
    evt = json.loads(m.value())
    if evt.get('type') == 'ToolCompleted':
        # TODO: look up ContinuationStore and emit TaskCreated/TaskReady
        print('[result-router] resume for', evt['payload'].get('task_id'))
    consumer.commit(m)
