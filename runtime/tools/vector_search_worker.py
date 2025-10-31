import os, json, time
from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv
load_dotenv()
ENV = os.environ.get

consumer = Consumer({
    'bootstrap.servers': ENV('KAFKA_BOOTSTRAP'),
    'group.id': 'tools.vector_search',
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
    if evt.get('type') == 'ToolRequested' and evt['payload'].get('tool') == 'vector_search':
        # Simulate work
        time.sleep(0.5)
        out = {
          "version":"1","type":"ToolCompleted","event_id":evt['event_id']+'c',
          "occurred_at":evt['occurred_at'],"tenant_id":evt['tenant_id'],"plan_id":evt['plan_id'],
          "payload":{"task_id":evt['payload']['task_id'],"tool_call_id":evt['payload']['tool_call_id'],
                     "outputs_ref":"s3://outputs/vs_out.json","metrics":{"lat_ms":500}}
        }
        producer.produce('tool.events', key=evt['plan_id'], value=json.dumps(out).encode('utf-8'))
        producer.flush()
    consumer.commit(m)
