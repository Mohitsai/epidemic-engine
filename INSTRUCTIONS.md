# Project Overview: Epidemic Engine Data Pipeline

As described in the syllabus (but not exactly) this project integrates several key technologies---Hadoop, Apache Spark, Apache Kafka, Apache Flink, and Apache Airflow---to build a comprehensive data pipeline for monitoring, processing, and analyzing health-related data to predict potential health risks.
The project is divided into 3 sub-projects in keeping with the grading in the syllabus. The sub-projects may have further sub-parts to ensure progress is continuously being made.
At the end, your team should have an end-to-end solution that simulates the core functionality of an \"Epidemic Engine.\"

## Project 1

### Part 1: Batch Data Analysis with Hadoop

#### Objective

Use Hadoop and MapReduce for batch processing of health event data to
uncover trends or patterns.

#### Getting Started

You have been provided a docker-compose.yml that will launch hadoop.
However, you have to run it as "root".
You have also been provided an example that will test the running instance of hadoop.
In order to run the example, you will need to use `make` as the commands are in a `Makefile`.
`make` is avaailable for every OS or, if you really want to be fancy, you can run it from a container.

What's tricky is that the example is written in java and your solution needs to be in Python.
In addition, the source code is not provided (it is probably available online just not supplied here).
We have provided you a template of how to run a python mapper & reducer.
You do need to supply the code in `word_count_python/mapper.py` & `word_count_python/mapper.py` if you want the python example to work.
I would recommend:

1. implement the word counter mapper and reducer
2. then, use the same pattern and change the mapper and reducer for each of the tasks

#### Provided

```
hadoop
├── docker-compose.yml -- launches hadoop
├── hadoop.env -- config file for hadoop that should "just work"
├── Makefile -- launches example & has a placeholder for your solution
├── simulated_health_events.csv -- data to operate on
├── word_count_java
│   ├── Dockerfile -- example container
│   ├── run.sh -- example runner
│   └── WordCount.jar -- java code for mapreduce
└── word_count_python
    ├── Dockerfile -- example container
    ├── mapper.py -- python mapper placeholder
    ├── reducer.py -- python reducer placeholder
    ├── run.sh -- example runner
    └── sources.list -- solution for getting python installed in the container
```

#### Tasks

* Write a MapReduce job to count the number of events by type.
* Aggregate events by location to identify high-risk areas.
* Update README.md with how to launch and run your solution.

#### Requirements

* When we git clone your repo, your solution should run using `make hadoop_solved`.
* Your `make target` should *not* launch hadoop

#### Tips

Here are some things that may be helpful while you are trying to build this solution.

* Your biggest challenge will likely be keeping track of the context all of your commands are running in.
  This can be super confusing so keep it in mind while debugging.
* If you get `PipeMapRed.waitOutputThreads(): subprocess failed with code 127` or something similar when trying to run your job, one of these is likely:
  * Your code isn't running properly, make sure it will run locally and locally in the container.
  You can get the log file by doing something like `yarn logs -applicationId application_1426769192808_0004` in the `namenode` see [stack overflow](https://stackoverflow.com/questions/29164388/hadoop-streaming-job-failing) for some hints.
  * You may need to restart your hadoop server w/ `<cmd> compose down && <cmd> compose up -d` because it is in a bad state.
* Handy hadoop commands (fyi `hdfs dfs` has been replaced by `hadoop fs`)
  * `hadoop fs -ls -R / | less # print the file listing recursively`
  * `hadoop fs -rm -r /output # remove the output dir`
  * `hadoop fs -get /local-output-reduced ./ # get a file from the hdfs filesystem`
  * `hadoop fs -put ./simulated_health_events.csv /input/ # put a file in hdfs to make it available to hadoop`

### Part 2: Real-time Stream Processing with Apache Flink

#### Objective

Implement real-time data processing using Apache Flink to identify immediate trends or anomalies in health event data.

#### Tasks

Canceled.

## Project 2
### Part 1: Data Ingestion and Categorization with Kafka (Due: Apr. 09)

#### Objective

Develop a Kafka-based system to ingest and categorize incoming health event data.

#### Tasks

* Create a Kafka Consumer:
  * Using the stream of health_events at `44.201.154.178:9092` on the topic `health_events`, collect the events.
* Using the events from your consumer, create 3 topics (`hospital_admission`, `emergency_incident`, `vaccination`) and broadcast the appropriate events using your own Kafka Producers.
* Using the events from your consumer, create 3 topics (`low`, `medium`, `high`) and broadcast the appropriate events using your own Kafka Producers.

#### Requirements

* Implement at least 6 producers for different event types.
* Ensure data integrity during ingestion and categorization.
* Create a comprehensive README detailing the design and operation of your Kafka setup.
* Everything must run in a container and be launchable with a docker-compose.yml (or Makefile)

#### Tips

* Check out https://github.com/bitnami/containers.git and `/bitnami-containers/bitnami/kafka` in particular.

### Part 2: Exploring with Apache Spark (Due: Apr. 16)

#### Objective

Utilize Apache Spark for deep analysis of health event data to identify trends and anomalies.

#### Tasks

* Data Loading:
  Load categorized data from Kafka topics into Spark DataFrames for processing.

* Exploratory Data Analysis (EDA):
  Conduct EDA to understand the distributions, correlations, and patterns within the data.
  Focus on key metrics like event frequency, geographical distribution, and event type relationships.

#### Requirements

* Detailed analysis notebook with visualizations of EDA and model performance metrics.
* Tools will continue to work even with new data

#### Tips

* Check out https://buspark.io/documentation/project-guides/eda_example
* You can expect some scaffolding to launch Apache Spark soon.

### Part 3: Advanced Analytics with Apache Spark (Due: Apr. 25)

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

#### Requirements

* Models are to be evaluated using appropriate validation techniques to ensure accuracy.
* Documentation on model choice, features used, and interpretation of results.

#### Tips

* You can expect some scaffolding to launch Apache Spark soon.

## Project 3 (Due: May 08)

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

#### Tips

* You can expect some scaffolding to launch Apache Airflow soon.

### Part 2: Data Visualization and Reporting

#### Objective

Create visual representations of the processed data to highlight key findings and trends.

#### Tasks

TBD

### Part 3: Final Integration, Connecting the Parts

Objective: Integrate all the components developed to establish an end-to-end data pipeline that simulates the Epidemic Engine, demonstrating the flow from data ingestion to visualization.

#### Tasks

* Ensure everything runs end to end.
  The EDA component is not meant to be part of the final "workflow"
