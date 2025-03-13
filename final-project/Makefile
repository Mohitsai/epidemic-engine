include .env

ARCH := $(shell uname -m)
UNAME := $(shell uname | tr '[:upper:]' '[:lower:]')
UUID := $(shell uuidgen | tr '[:upper:]' '[:lower:]')
KIND_CLUSTER := "team3-cluster"

COLOUR_GREEN=\033[0;32m
COLOUR_RED=\033[0;31m
COLOUR_BLUE=\033[0;34m
END_COLOUR=\033[0m

ifeq ($(ARCH), "arm64")
	ARCH := "arm64"
endif

.PHONY: bootstrap-k8s-tools start-kind build-kafka-consumer

test:
	@echo "$(COLOUR_GREEN)Test Passed$(END_COLOUR)"

bootstrap-k8s-tools:
	@echo "$(COLOUR_BLUE)Checking if kind exists...$(END_COLOUR)"
	@if ! command -v kind >/dev/null 2>&1; then \
		echo "kind not found, installing"; \
		curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-$(UNAME)-$(ARCH); \
		chmod +x kind && \
		sudo mv kind /usr/local/bin/kind; \
	fi

	@echo "$(COLOUR_BLUE)Checking if kubectl exists...$(END_COLOUR)"
	@if ! command -v kubectl >/dev/null 2>&1; then \
		echo "kubectl not found, installing"; \
		curl -LO "https://storage.googleapis.com/kubernetes-release/release/$$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/$(UNAME)/$(ARCH)/kubectl"; \
		chmod +x kubectl && \
		sudo mv kubectl /usr/local/bin/kubectl; \
	fi

start-kind: bootstrap-k8s-tools
	kind delete cluster --name $(KIND_CLUSTER) || true
	kind create cluster --name $(KIND_CLUSTER) 

build-kafka-consumer:
	@echo "$(COLOUR_GREEN)Building $(PYTHON_KFK_CONS_IMAGE)....$(END_COLOUR)"
	docker build -t $(PYTHON_KFK_CONS_IMAGE):$(UUID) ./kafka-consumer/
	@echo "$(COLOUR_GREEN)Built image $(PYTHON_KFK_CONS_IMAGE):$(UUID)$(END_COLOUR)"

build-ml-model:
	@echo "$(COLOUR_BLUE)Building $(SPARK_IMAGE)....$(END_COLOUR)"
	docker build -t $(SPARK_IMAGE):$(UUID) ./ml-model/
	@echo "$(COLOUR_GREEN)Built image $(SPARK_IMAGE):$(UUID)$(END_COLOUR)"

build-flask-app:
	@echo "$(COLOUR_BLUE)Building $(PYTHON_FLSK_APP_IMAGE)....$(END_COLOUR)"
	docker build -t $(PYTHON_FLSK_APP_IMAGE):$(UUID) ./flask-app/
	@echo "$(COLOUR_GREEN)Built image $(PYTHON_FLSK_APP_IMAGE):$(UUID)$(END_COLOUR)"

deploy-k8s: start-kind build-kafka-consumer build-flask-app
	@echo "$(COLOUR_BLUE)Deploying to kind k8s cluster....$(END_COLOUR)"
	kind load docker-image $(PYTHON_KFK_CONS_IMAGE):$(UUID) --name $(KIND_CLUSTER)
	kind load docker-image $(PYTHON_FLSK_APP_IMAGE):$(UUID) --name $(KIND_CLUSTER)
	kind load docker-image $(SPARK_IMAGE):$(UUID) --name $(KIND_CLUSTER)
	@echo "$(COLOUR_GREEN)Loaded all images$(END_COLOUR)"

deploy-dc:
	@echo "$(COLOUR_BLUE)Deploying to docker-compose....$(END_COLOUR)"
	docker-compose up -d
	@echo "$(COLOUR_GREEN)Docker-compose up and running$(END_COLOUR)"

generate-models:
	@echo "$(COLOUR_RED)Running various models....$(END_COLOUR)"

	@echo "$(COLOUR_BLUE)Running anomaly-detection-model....$(END_COLOUR)"
	docker compose exec spark-master spark-submit --master spark://spark-master:7077 ml-model/anomaly-detection-model.py

	@echo "$(COLOUR_BLUE)Running model....$(END_COLOUR)"
	docker compose exec spark-master spark-submit --master spark://spark-master:7077 ml-model/risk-prediction-model.py

	@echo "$(COLOUR_GREEN)Finished running all models, outputs are available in ml-model/outputs folder$(END_COLOUR)"

run-prediction:
	@echo "$(COLOUR_BLUE)Running custom prediction on user-defined data and model....$(END_COLOUR)"
	python3 user-interaction.py

generate-ver-file:
ifeq ("$(wildcard $(VER_FILE))","")
	@echo "0" > "$(VER_FILE)"
else
endif

