DOCKER_NETWORK = hadoop_default
ENV_FILE = hadoop.env
current_branch := 2.0.0-hadoop3.2.1-java8
CONTAINER_CMD = docker
NETWORK_ENV_PARAMS = --network ${DOCKER_NETWORK} --env-file ${ENV_FILE}
RUN_PARAMS = ${NETWORK_ENV_PARAMS} bde2020/hadoop-base:$(current_branch)

# Adding a shell session for testing
get-sh:
	$(CONTAINER_CMD) build -t hadoop-event-counter ./event_counter
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input  || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-event-counter hadoop fs -copyFromLocal -f /app/simulated_health_events.csv /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-event-counter

	$(CONTAINER_CMD) run -it $(RUN_PARAMS) sh

wordcount-java:
	$(CONTAINER_CMD) build -t hadoop-wordcount-java ./word_count_java
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -copyFromLocal -f /opt/hadoop-3.2.1/README.txt /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-wordcount-java
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/*
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

build-hadoop-customized-images:
# Need this to run python as it is not preinstalled in any of the components - https://github.com/big-data-europe/docker-hadoop/issues/95#issuecomment-771540372
	$(CONTAINER_CMD) build -t eengine-hadoop-base --target=eengine-hadoop-base .
	$(CONTAINER_CMD) build -t eengine-hadoop-namenode --target=eengine-hadoop-namenode .
	$(CONTAINER_CMD) build -t eengine-hadoop-datanode --target=eengine-hadoop-datanode .
	$(CONTAINER_CMD) build -t eengine-hadoop-resourcemanager --target=eengine-hadoop-resourcemanager .
	$(CONTAINER_CMD) build -t eengine-hadoop-nodemanager --target=eengine-hadoop-nodemanager .
	$(CONTAINER_CMD) build -t eengine-hadoop-historyserver --target=eengine-hadoop-historyserver .

event-counter:
	$(CONTAINER_CMD) build -t hadoop-event-counter ./event_counter
	chmod +x add-python.sh
	./add-python.sh
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input  || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-event-counter hadoop fs -copyFromLocal -f /app/simulated_health_events.csv /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-event-counter
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/*
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

location-mapreducer: 
	$(CONTAINER_CMD) build -t hadoop-location-mapreducer ./location_mapreducer
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input  || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-location-mapreducer hadoop fs -copyFromLocal -f /app/simulated_health_events.csv /input/
	$(CONTAINER_CMD) run ${NETWORK_ENV_PARAMS} hadoop-location-mapreducer
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/*
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

hadoop_solved: event-counter location-mapreducer
	