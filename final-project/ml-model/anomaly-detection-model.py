import datetime
from numpy import array, sqrt

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, unix_timestamp, expr, when
from pyspark.sql.types import FloatType

from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler, OneHotEncoder
from pyspark.ml.evaluation import ClusteringEvaluator, MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Anomaly Detection Model") \
    .getOrCreate()

# Load the data
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true") \
    .load("/opt/bitnami/spark/ml-model/inputs/1m_health_events_dataset.csv") \
    .withColumn("timestamp_unix", unix_timestamp("Timestamp"))

train_df, test_df = df.randomSplit([0.7, 0.3], seed=42)

# Index and encode categorical features
indexer_event = StringIndexer(inputCol="EventType", outputCol="EventType_Index")
indexer_location = StringIndexer(inputCol="Location", outputCol="Location_Index")

# Convert 'Severity' to a numerical scale
severity_scale = {"low": 1, "medium": 2, "high": 3}
train_df = train_df.withColumn("Severity_Num", when(col("Severity") == "low", severity_scale["low"])
                                                        .when(col("Severity") == "medium", severity_scale["medium"])
                                                        .when(col("Severity") == "high", severity_scale["high"]))
test_df = test_df.withColumn("Severity_Num", when(col("Severity") == "low", severity_scale["low"])
                                                      .when(col("Severity") == "medium", severity_scale["medium"])
                                                      .when(col("Severity") == "high", severity_scale["high"]))

# Assemble features into a single vector column
assembler = VectorAssembler(inputCols=["EventType_Index", "Location_Index", "Severity_Num"], outputCol="features")

# Scale the features
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")

# Define the KMeans model
kmeans = KMeans().setK(9).setSeed(7).setFeaturesCol("scaledFeatures")

# Build the pipeline
pipeline = Pipeline(stages=[indexer_event, indexer_location, assembler, scaler, kmeans])

# Define a parameter grid
paramGrid = (ParamGridBuilder()
             .addGrid(kmeans.k, [12])  # Number of clusters
             .addGrid(scaler.withStd, [True, False])  # Standard deviation scaling
             .build())

# Define the evaluator
evaluator = ClusteringEvaluator(predictionCol="prediction", featuresCol="scaledFeatures", metricName="silhouette")

# Set up the CrossValidator
crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=evaluator,
                          numFolds=9)  # Adjusted for demonstration

# Run cross-validation on the training data, and choose the best set of parameters.
cvModel = crossval.fit(train_df)

# Fetch the best model
model = cvModel.bestModel
bestKMeansModel = model.stages[-1]  # The last stage is KMeans in the pipeline

# Make predictions on the test data
predictions = model.transform(test_df)

# Now choose an anomaly cluster as before (this part would be manual and interpretive)
anomaly_cluster = 1  # This needs to be checked based on new cluster centers
predictions = predictions.withColumn("predicted_Is_Anomaly", (col("prediction") == anomaly_cluster).cast("double"))

# Calculate Accuracy and F1 Score (as before, or consider using binary evaluators)
evaluator_accuracy = MulticlassClassificationEvaluator(labelCol="Is_Anomaly", predictionCol="predicted_Is_Anomaly", metricName="accuracy")
accuracy = evaluator_accuracy.evaluate(predictions)

evaluator_f1 = MulticlassClassificationEvaluator(labelCol="Is_Anomaly", predictionCol="predicted_Is_Anomaly", metricName="f1")
f1_score = evaluator_f1.evaluate(predictions)

print(f"Best number of clusters: {bestKMeansModel.getK()}")
print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1_score}")
predictions.show(25)
# Save the model and results
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
model_path = f"/opt/bitnami/spark/ml-model/saved-models/anomaly_detection_model"
model.write().overwrite().save(model_path)

output_path = f"/opt/bitnami/spark/ml-model/outputs/predictions_{current_time}.csv"
predictions.select("EventType", "Timestamp", "Location", "Severity", "Details", "Is_Anomaly", "predicted_Is_Anomaly") \
    .write.format("csv").option("header", "true").mode("overwrite").save(output_path)
