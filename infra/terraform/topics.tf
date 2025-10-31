resource "confluent_kafka_topic" "plan_events" { topic_name = "plan.events" partitions_count = 6 rest_endpoint = var.cluster_id kafka_cluster { id = var.cluster_id } }
resource "confluent_kafka_topic" "task_events" { topic_name = "task.events" partitions_count = 12 rest_endpoint = var.cluster_id kafka_cluster { id = var.cluster_id } }
resource "confluent_kafka_topic" "tool_events" { topic_name = "tool.events" partitions_count = 12 rest_endpoint = var.cluster_id kafka_cluster { id = var.cluster_id } }
resource "confluent_kafka_topic" "blackboard_events" { topic_name = "blackboard.events" partitions_count = 6 rest_endpoint = var.cluster_id kafka_cluster { id = var.cluster_id } }
