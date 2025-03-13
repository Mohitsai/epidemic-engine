from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofweek, dayofmonth, month, year, unix_timestamp
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import datetime

spark = SparkSession.builder \
    .appName("KafkaToSpark") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
    .getOrCreate()

df = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load("/opt/bitnami/spark/ml-model/inputs/1m_health_events_dataset.csv")\
    .coalesce(5)

df.cache()
df.printSchema()
print("This datasets consists of {} rows.".format(df.count()))


df = df.withColumn("Hour", hour(col("Timestamp"))) \
       .withColumn("DayOfWeek", dayofweek(col("Timestamp"))) \
       .withColumn("DayOfMonth", dayofmonth(col("Timestamp"))) \
       .withColumn("Month", month(col("Timestamp"))) \
       .withColumn("Year", year(col("Timestamp"))) \
       .withColumn("TimestampUnix", unix_timestamp(col("Timestamp")))

df.cache()

# Encode categorical columns using StringIndexer
event_indexer = StringIndexer(inputCol="EventType", outputCol="EventTypeIndex")
location_indexer = StringIndexer(inputCol="Location", outputCol="LocationIndex")
severity_indexer = StringIndexer(inputCol="Severity", outputCol="SeverityIndex")

# Assemble features into a single vector column
feature_columns = ["EventTypeIndex", "LocationIndex", "SeverityIndex", "Hour", "DayOfWeek", "DayOfMonth", "Month", "Year", "TimestampUnix"]
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Define the classifier with additional GPU-specific configurations if needed
classifier = RandomForestClassifier(labelCol="Is_Anomaly", featuresCol="features", numTrees=100)

# Create a pipeline
pipeline = Pipeline(stages=[event_indexer, location_indexer, severity_indexer, assembler, classifier])

# Create a parameter grid for hyperparameter tuning
param_grid = ParamGridBuilder() \
    .addGrid(classifier.maxDepth, [10]) \
    .addGrid(classifier.numTrees, [50]) \
    .build()

# Define a cross-validator
cross_validator = CrossValidator(estimator=pipeline,
                                 estimatorParamMaps=param_grid,
                                 evaluator=MulticlassClassificationEvaluator(labelCol="Is_Anomaly", metricName="accuracy"),
                                 numFolds=5)

# Split data into training and test sets
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)

# Train the model
cv_model = cross_validator.fit(train_data)

# Make predictions using the trained model
predictions = cv_model.transform(test_data)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="Is_Anomaly", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

#save the model
model_path = "/opt/bitnami/spark/ml-model/saved-models/risk_prediction_model"
cv_model.bestModel.write().overwrite().save(model_path)


# Specifying the output path, which might already exist
output_path = "/opt/bitnami/spark/ml-model/outputs/predictions.csv"

# Generate a timestamp
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Specifying the output path with a timestamp
output_path = f"/opt/bitnami/spark/ml-model/outputs/predictions_{current_time}.csv"

# Using write operation with overwrite mode
predictions.select("EventType", "Timestamp", "Location", "Severity", "Details", "Is_Anomaly") \
    .write.format("csv") \
    .option("header", "true") \
    .mode("overwrite") \
    .save(output_path)
