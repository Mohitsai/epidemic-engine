#!/bin/bash

KAFKA_BROKER="44.201.154.178:9092"
KAFKA_TOPICS_CMD="kafka-topics.sh" #path of kafka-topics.sh

echo "Topic: hospital_admission"
$KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic hospital_admission --create --if-not-exists --replication-factor 1 --partitions 3

echo "Topic: emergency_incident"
KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic emergency_incident --create --if-not-exists --replication-factor 1 --partitions 3

echo "Topic: vaccination"
KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic vaccination --create --if-not-exists --replication-factor 1 --partitions 3

echo "Topic: low"
KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic low --create --if-not-exists --replication-factor 1 --partitions 3

echo "Topic: medium"
KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic medium --create --if-not-exists --replication-factor 1 --partitions 3

echo "Topic: high"
KAFKA_TOPICS_CMD --bootstrap-server $KAFKA_BROKER --topic high --create --if-not-exists --replication-factor 1 --partitions 3

echo "All topics created successfully."