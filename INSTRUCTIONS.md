# Project Overview: Epidemic Engine Data Pipeline

As described this project integrates several key technologies---Hadoop, Apache Spark, Apache Kafka, Apache Flink, and Apache Airflow---to build a comprehensive data pipeline for monitoring, processing, and analyzing health-related data to predict potential health risks.

At the end, you should have an end-to-end solution that simulates the core functionality of an \"Epidemic Engine.\"

## Project 1

### Part 1: Batch Data Analysis with Hadoop

#### Objective

Use Hadoop and MapReduce for batch processing of health event data to
uncover trends or patterns.


### Part 2: Real-time Stream Processing with Apache Flink

#### Objective

Implement real-time data processing using Apache Flink to identify immediate trends or anomalies in health event data.

## Project 2
### Part 1: Data Ingestion and Categorization with Kafka (Due: Apr. 09)

#### Objective

Develop a Kafka-based system to ingest and categorize incoming health event data.

#### Tasks

* Create a Kafka Consumer:
  * Using the stream of health_events at `44.201.154.178:9092` on the topic `health_events`, collect the events.
* Using the events from your consumer, create 3 topics (`hospital_admission`, `emergency_incident`, `vaccination`) and broadcast the appropriate events using your own Kafka Producers.
* Using the events from your consumer, create 3 topics (`low`, `medium`, `high`) and broadcast the appropriate events using your own Kafka Producers.

### Part 2: Exploring with Apache Spark (Due: Apr. 16)

#### Objective

Utilize Apache Spark for deep analysis of health event data to identify trends and anomalies.

#### Tasks

* Data Loading:
  Load categorized data from Kafka topics into Spark DataFrames for processing.

* Exploratory Data Analysis (EDA):
  Conduct EDA to understand the distributions, correlations, and patterns within the data.
  Focus on key metrics like event frequency, geographical distribution, and event type relationships.

### Part 3: Advanced Analytics with Apache Spark

#### Objective

Predict potential health risks with Apache Spark.
A stream of "outcomes" will be launched as well as a set of labeled historical data provided.
However, the more information you have collected in the prior parts the better your models will be.

#### Tasks

* Anomaly Detection:
  Implement an anomaly detection model to identify unusual patterns of events that could signify emerging health risks.

* Risk Prediction Model:
  Develop a predictive model using Spark MLlib to forecast potential health risks based on historical data trends.
  Consider features like event type, location, and time of year.

## Project 3

### Part 1: Workflow Orchestration with Apache Airflow

#### Objective

Orchestrate the entire data pipeline using Apache Airflow, ensuring each component is executed efficiently and in the correct order.
Each of these tasks should be the "lightweight" version.
As in some attempt at error handing but it doesn't have to be perfect.

#### Tasks

* Define Airflow DAGs:
  * Create DAGs representing the workflow, starting from data ingestion with Kafka producers, categorization, loading into Spark, analysis, and finally, risk prediction.
* Task Scheduling and Dependencies:
  * Schedule tasks ensuring that dependencies are met, such as not starting the Spark analysis before Kafka data ingestion and categorization are completed.
* Error Handling and Alerts:
  * Implement error handling within your DAGs to manage failures in tasks. Set up email alerts or notifications for task failures or retries.
* Monitoring and Optimization:
    Utilize Airflow's monitoring tools to track pipeline performance and identify bottlenecks or inefficiencies. Document any adjustments made to optimize the workflow.

### Part 2: Data Visualization and Reporting

#### Objective

Create visual representations of the processed data to highlight key findings and trends.

### Part 3: Final Integration, Connecting the Parts

Objective: Integrate all the components developed to establish an end-to-end data pipeline that simulates the Epidemic Engine, demonstrating the flow from data ingestion to visualization.
