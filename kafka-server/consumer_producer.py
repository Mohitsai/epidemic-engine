from kafka import KafkaConsumer, KafkaProducer
import json
import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable


def categorize_event(event):
    # EventType-based categorization
    return event["EventType"]


def categorize_severity(event):
    # Severity-based categorization
    return event["Severity"]


def is_broker_reachable(bootstrap_servers):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers, request_timeout_ms=500
        )
        metadata = admin_client.list_topics()
        admin_client.close()
        return True
    except NoBrokersAvailable:
        return False


# Source data
source_bootstrap_servers = ["44.201.154.178:9092"]
source_topic = "health_events"
# kafka consumer
print("Initializing consumer...")
source_consumer = KafkaConsumer(
    source_topic,
    bootstrap_servers=source_bootstrap_servers,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# Destination
dest_broker = "kafka:9092"
# Check if local broker is reachable
check_interval = 5

while True:
    if is_broker_reachable(dest_broker):
        print("Destination Broker is reachable.")
        break
    else:
        print(
            "Destination Broker is not reachable. Retrying in {} seconds...".format(check_interval)
        )
        time.sleep(check_interval)


dest_producer = KafkaProducer(
    bootstrap_servers=dest_broker,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Topics
EVENT_TYPES = {"hospital_admission", "emergency_incident", "vaccination"}
SEVERITY = {"low", "medium", "high"}
num_partitions = 3
replication_factor = 1

admin_client = KafkaAdminClient(bootstrap_servers=dest_broker)

print("Creating destination topics")
for topic in EVENT_TYPES.union(SEVERITY):
    try:
        admin_client.create_topics(
            new_topics=[
                NewTopic(
                    name=topic,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor,
                )
            ]
        )
    except TopicAlreadyExistsError:
        print(f"Topic {topic} already exists, skipping....")

print("Topics created successfully")
admin_client.close()

# Consume events from source
for message in source_consumer:
    event = message.value
    print(f"Received event: {event}")

    if categorize_event(event) in EVENT_TYPES:
        dest_producer.send(categorize_event(event), event)
        dest_producer.flush()
    else:
        print(f"EventType not recognized: {event}")

    if categorize_severity(event) in SEVERITY:
        dest_producer.send(categorize_severity(event), event)
        dest_producer.flush()
    else:
        print(f"Severity not recognized: {event}")

# Received event: {'EventType': 'emergency_incident', 'Timestamp': '2024-04-09 11:44:01', 'Location': 'New York', 'Severity': 'high', 'Details': 'This is a simulated emergency_incident event.'}
# Received event: {'EventType': 'general_health_report', 'Timestamp': '2024-04-09 11:44:05', 'Location': 'Boston', 'Severity': 'medium', 'Details': 'This is a simulated general_health_report event.'}
