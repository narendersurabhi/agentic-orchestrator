# Example service account; add ACLs per topic with confluent_kafka_acl resources
resource "confluent_service_account" "workers" { display_name = "workers" description = "Agent and tool workers" }
