# Epidemic Engine – Healthcare Data Pipeline

## Project Overview
The **Epidemic Engine** is an **end-to-end healthcare data pipeline** designed to efficiently process **real-time streaming and batch data** for public health monitoring. The system enables **real-time ingestion, processing, storage, predictive analytics, and visualization** of healthcare event data. 

Built using a **fully containerized approach** with **Docker and Docker Compose**, the pipeline ensures **scalability, modularity, and fault tolerance**, handling over **1 million records** effectively. The workflow is managed with **Apache Airflow**, and the predictive analytics component leverages **Apache Spark ML** for outbreak prediction and health risk detection with **93.7% accuracy**.

## Key Features
- **Real-Time Streaming & Batch Processing**:
  - Uses **Apache Kafka** for continuous ingestion of healthcare event data.
  - Processes large-scale data using **Hadoop MapReduce** for batch analysis.
- **Fully Containerized Execution**:
  - Runs as a modular system with **Docker and Docker Compose**.
  - Includes **automatic health checks** and **failure recovery**.
- **Workflow Automation & Orchestration**:
  - **Apache Airflow** manages job scheduling and dependencies.
- **Predictive Analytics with Machine Learning**:
  - Built **Spark ML models** (GBT Classifier) for epidemic outbreak detection.
  - Achieved **93.7% accuracy** in identifying health risks.
- **Visualization & Web Interface**:
  - **Power BI & Jupyter Notebook visualizations**.
  - **Live graphs** served via a web dashboard (**Flask-based UI**).
- **Automated Model Retraining & Deployment**:
  - Machine learning model **retrained in production** without downtime.
- **Robust Storage & Data Management**:
  - Uses **PostgreSQL** for structured storage.
  - Data stored in **Parquet and Delta Lake formats** for efficient querying.

---

## System Architecture
**1️⃣ Data Ingestion**  
- **Apache Kafka**: Streams real-time healthcare event data (Producer is no longer running permanently).
- **Dockerized Kafka Consumers**: Store incoming messages into **PostgreSQL**.
- **Airflow DAGs** trigger ETL jobs automatically.

**2️⃣ Batch Data Processing**  
- **Hadoop MapReduce**: Processes 1M+ historical records.
- **Apache Spark (PySpark)**: Runs transformations & feature engineering.

**3️⃣ Predictive Analytics**  
- **Spark ML (GBT Classifier)** for outbreak prediction.
- **ML pipeline includes** feature extraction, encoding, and hyperparameter tuning.
- **Incremental model retraining** using new data.

**4️⃣ Data Storage & Management**  
- **PostgreSQL**: Stores structured data.
- **Parquet & Delta Lake**: Optimized for analytics & historical storage.

**5️⃣ Visualization & Monitoring**  
- **Flask Web App**: Displays real-time dashboards.
- **Power BI & Jupyter Notebooks** for EDA & insights.

---

## Setup & Deployment
### **1️⃣ Prerequisites**
- **Docker Desktop** installed & running ([Download](https://www.docker.com/products/docker-desktop/)).
- **Python 3.8+** installed.
- **Apache Airflow** installed & configured.
- **Jupyter Notebook** installed.
- **Hadoop & Spark** (configured inside Docker).

### **2️⃣ Cloning the Repository**
```bash
git clone https://github.com/your-username/epidemic-engine.git
cd epidemic-engine
```

### **3️⃣ Running Kafka & PostgreSQL for Real-Time Streaming**
```bash
cd kafka-server
docker compose up -d
```
**Note:** The Kafka producer is no longer running permanently, meaning **new data is not continuously ingested**. The system will process existing records but will not receive fresh event streams in real-time.

### **4️⃣ Running Batch Processing with Hadoop**
```bash
cd hadoop
docker-compose up --build
make hadoop_solved
```

### **5️⃣ Running Data Processing & Machine Learning with Spark**
```bash
cd spark-explore
docker compose up -d
```
After starting Spark, check the logs of the `ed-pyspark-jupyter-lab` container to find the **Jupyter Notebook link** and access the EDA notebook.

### **6️⃣ Running Model Training & Retraining**
```bash
cd machine-learning
jupyter notebook
```
Open **sparkMLModel.ipynb** and **sklearnML.ipynb** for model training & evaluation.

To **retrain the model**, run:
```bash
python retrainModel.py
```

### **7️⃣ Running the Final Integrated System**
```bash
cd final
docker compose up -d
```
Visit **http://localhost:8080/** to view the web-based visualizations.

---

## Machine Learning Models
### **1️⃣ sklearnML.ipynb (Scikit-Learn ML Model)**
- Implements **Decision Tree & XGBoost Classifiers**.
- Performs **feature engineering** (hour of event, day of week, etc.).
- Uses **GridSearchCV** for hyperparameter tuning.
- Evaluates models using **confusion matrix, precision, recall, and F1-score**.

### **2️⃣ sparkMLModel.ipynb (Spark ML Model)**
- Uses **StringIndexer, Encoder, and VectorAssembler** for preprocessing.
- Trains **Logistic Regression, Decision Tree, Random Forest, and GBT Classifiers**.
- **GBT Classifier** achieves the highest accuracy **(93.7%)**.

### **3️⃣ Real-Time Model Prediction**
- **kafka-data-predictor.py**: Predicts from Kafka streaming data.
- **dataset-prediction.py**: Predicts from batch CSV datasets.

---

## Visualization & Web Dashboard
### **1️⃣ Jupyter Notebook (Exploratory Data Analysis)**
- Run **EDA.ipynb** to generate initial insights.

### **2️⃣ Flask Web Dashboard (Real-Time Graphs)**
- **http://localhost:8080/**
- Displays:
  - Live streaming event data.
  - Historical outbreak trends.
  - Predicted future outbreak events.

---

## Workflow Automation with Apache Airflow
### **1️⃣ Starting Airflow DAGs**
```bash
cd airflow
docker compose up -d
```
Airflow DAGs handle:
- **Automated ingestion from Kafka**.
- **Batch processing & transformations**.
- **Scheduled model retraining**.

### **2️⃣ Airflow UI Access**
Visit **http://localhost:8081/** to monitor workflow execution.

---

## Contributing & Usage
- **Use it fairly**: Modify and adapt as needed.
- **Ensure proper configuration**: Adjust paths & credentials before deploying.
- **Star ⭐ the repo** if you found it useful!

---

## Contact
Feel free to reach out via:
- **[LinkedIn](https://www.linkedin.com/in/mohitsaigutha/)**
- **[Email](mailto:mohit.sai6@gmail.com)**

---

**© 2025 Mohit Sai Gutha** | Built with ❤️ using **Kafka, Spark, Hadoop & Airflow**
