import os, json, uuid, time
from confluent_kafka import Producer
from dotenv import load_dotenv
load_dotenv()
p = Producer({'bootstrap.servers': os.environ['KAFKA_BOOTSTRAP'],
              'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL','SASL_SSL'),
              'sasl.mechanisms': os.environ.get('KAFKA_SASL_MECHANISM','PLAIN'),
              'sasl.username': os.environ['KAFKA_SASL_USERNAME'],
              'sasl.password': os.environ['KAFKA_SASL_PASSWORD']})
def emit(topic, key, evt):
    p.produce(topic, key=key, value=json.dumps(evt).encode('utf-8'))
    p.flush()

def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

plan_id = f'plan_{uuid.uuid4().hex[:8]}'

plan_created = {
  "version":"1","type":"PlanCreated","event_id":uuid.uuid4().hex,"occurred_at":now(),
  "tenant_id":"t_demo","plan_id":plan_id,"payload":{
    "graph":{"nodes":[
      {"id":"t_retrieve","kind":"task","type":"retrieve","deps":[]},
      {"id":"tc_vs_1","kind":"tool","tool":"vector_search","deps":["t_retrieve"]},
      {"id":"t_draft","kind":"task","type":"draft","deps":["tc_vs_1"]},
      {"id":"t_finish","kind":"task","type":"aggregate","deps":["t_draft"]}
    ],"edges":[["t_retrieve","tc_vs_1"],["tc_vs_1","t_draft"],["t_draft","t_finish"]]},
    "constraints":{"max_depth":4,"max_width":12,"budget_tokens":120000}
  }
}
emit('plan.events', plan_id, plan_created)

# Emit initial TaskCreated and ToolRequested
emit('task.events', plan_id, {
  "version":"1","type":"TaskCreated","event_id":uuid.uuid4().hex,"occurred_at":now(),
  "tenant_id":"t_demo","plan_id":plan_id,"payload":{
    "task_id":"t_retrieve","type":"retrieve","inputs_ref":"s3://inputs/retrieve.json","deps":[]
  }
})
emit('tool.events', plan_id, {
  "version":"1","type":"ToolRequested","event_id":uuid.uuid4().hex,"occurred_at":now(),
  "tenant_id":"t_demo","plan_id":plan_id,"payload":{
    "task_id":"t_draft","tool_call_id":"tc_vs_1","tool":"vector_search","inputs_ref":"s3://inputs/vs.json","deps":["t_retrieve"],"continuation":"cont_demo"
  }
})
print('Seed plan emitted:', plan_id)
