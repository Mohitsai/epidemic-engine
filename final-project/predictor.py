import argparse
import datetime
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, from_json, year, quarter
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.ml import PipelineModel

# Setup argparse
parser = argparse.ArgumentParser(description='Predict anomalies using a trained model.')
parser.add_argument("--mode", required=True, choices=['Kafka', 'File'], help="Mode of data input: Kafka or File")
parser.add_argument("--starting-offsets", default="earliest", choices=["earliest", "latest"], help="Starting offset for Kafka")
parser.add_argument("--input-file", help="Data source for prediction if mode is File")
parser.add_argument("--model-name", required=True, help="Path to the trained model")
args = parser.parse_args()

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Anomaly Detection Prediction") \
    .getOrCreate()

# Define schema
defined_schema = StructType([
    StructField("EventType", StringType()),
    StructField("Timestamp", TimestampType()),
    StructField("Location", StringType()),
    StructField("Severity", StringType()),
    StructField("Details", StringType())
])

# Load the trained model
model_path = f"/opt/bitnami/spark/ml-model/saved-models/{args.model_name}"
model = PipelineModel.load(model_path)

if args.mode == "Kafka":
    kafka_broker = "44.201.154.178:9092"
    topic = "health_events"

    kafka_source = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kafka_broker) \
        .option("subscribe", topic) \
        .option("startingOffsets", args.starting_offsets) \
        .load()

    kafka_stream = kafka_source.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", defined_schema).alias("data")).select("data.*")

    print("Making predictions on Kafka stream...")
    predictions = model.transform(kafka_stream)
    query = predictions.writeStream.outputMode("append").format("console").start()
    query.awaitTermination()
else:
    # Read the data from a file
    data_path = f"/opt/bitnami/spark/ml-model/inputs/{args.input_file}"
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(data_path) \
        .coalesce(5)

    df.cache()
    df.printSchema()
    print(f"This datasets consists of {df.count()} rows.")

# Load the trained model
model_path = f"/opt/bitnami/spark/ml-model/saved-models/{args.model_name}"
model = PipelineModel.load(model_path)

# Make predictions
print("Making predictions...")
predictions = model.transform(df)

# Adding predictions to the DataFrame
df_with_predictions = predictions.withColumnRenamed("prediction", "Is_Anomaly")

# Show schema and preview results
df_with_predictions.printSchema()
df_with_predictions.select("EventType", "Timestamp", "Location", "Severity", "Details", "Is_Anomaly").show(truncate=False)

# Store output in outputs folder
output_path = "/opt/bitnami/spark/ml-model/outputs/predictions.csv"
print(f"Saving predictions to {output_path}...")
df_with_predictions.select("EventType", "Timestamp", "Location", "Severity", "Details", "Is_Anomaly").write.format("csv").option("header", "true").save(output_path)

# make visualization
df = df_with_predictions.select("EventType", "Timestamp", "Location", "Severity", "Details", "Is_Anomaly")

# Convert Timestamp to actual timestamp type and filter data
df = df.withColumn("Timestamp", to_timestamp(col("Timestamp")))
df = df.filter((df.EventType == "hospital_admission") & (df.Is_Anomaly == 1))

# Convert Spark DataFrame to Pandas DataFrame for easier manipulation
pdf = df.select("Timestamp", "Location", "Severity").toPandas()

# Define severity levels for plotting and colors
severity_levels = {'low': 1, 'medium': 2, 'high': 3}
colors = {
    'Paris': 'blue', 
    'Boston': 'green', 
    'New York': 'red', 
    'Chicago': 'purple',
    'Los Angeles': 'orange',
    'Bordeaux': 'brown',
    'Tokyo': 'pink',
    'Berlin': 'grey'
}

# Determine the layout of subplots
cities = pdf['Location'].unique()
n_cities = len(cities)
n_cols = 4  # Number of columns in the subplot grid
n_rows = (n_cities + n_cols - 1) // n_cols  # Compute the number of rows needed

# Create the figure with subplots
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(15, 5 * n_rows), sharex=True, sharey=True)
fig.subplots_adjust(hspace=0.5, wspace=0.3)

# Flatten the axes array for easier iteration
axes = axes.flatten()

# Plot each city's data in its own subplot
for idx, city in enumerate(cities):
    ax = axes[idx]
    city_data = pdf[pdf['Location'] == city]
    city_data = city_data.sort_values(by='Timestamp')
    city_data['SeverityLevel'] = city_data['Severity'].map(severity_levels)
    ax.plot(city_data['Timestamp'], city_data['SeverityLevel'], color=colors[city], marker='o', label=city)
    ax.set_title(city)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Low', 'Medium', 'High'])

# Turn off axes for any unused subplots
for ax in axes[n_cities:]:
    ax.axis('off')

plt.suptitle('Timeline of Outbreak Events by Severity and Location')

# Generate a timestamp
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Specifying the output path with a timestamp
output_path_1 = f"/opt/bitnami/spark/ml-model/outputs/plot_outbreak_timeline_{current_time}.png"

plt.savefig(output_path_1)



# Filter for outbreak events
outbreak_df = df.filter((df.EventType == "hospital_admission") & (df.Is_Anomaly == 1))

# Extract Year and Quarter from Timestamp
outbreak_df = outbreak_df.withColumn("Year", year(col("Timestamp")))
outbreak_df = outbreak_df.withColumn("Quarter", quarter(col("Timestamp")))

# Group by Year, Quarter, and Location
quarterly_counts = outbreak_df.groupBy("Location", "Year", "Quarter").count()

# Collect the data for plotting
plot_data = quarterly_counts.orderBy("Year", "Quarter").collect()


results = defaultdict(list)

for row in plot_data:
    location = row['Location']
    # Create a date object representing the first month of the quarter for plotting
    date = pd.to_datetime(f"{row['Year']}-{(row['Quarter'] - 1) * 3 + 1:02d}-01")
    results[location].append((date, row['count']))

# Create the plot
fig, ax = plt.subplots(figsize=(14, 7))

for location, data in results.items():
    if data:  # Check if there is any data for the location
        dates, counts = zip(*sorted(data))
        ax.plot(dates, counts, marker='o', linestyle='-', label=f'{location}')

# Formatting the plot
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set major ticks to quarterly
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
plt.xticks(rotation=45)
plt.xlabel('Time (Year-Quarter)')
plt.ylabel('Count of Outbreak Events')
plt.title('Quarterly Count of Outbreak Events by Location')
plt.legend(title='Location')
plt.grid(True)
plt.tight_layout()

output_path_2 = f"/opt/bitnami/spark/ml-model/outputs/plot_outbreak_quarterly_{current_time}.png"
plt.savefig(output_path_2)

spark.stop()
