from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import os
from pyspark.ml.feature import VectorAssembler
import numpy as np
# Load training data
from pyspark.python.pyspark.shell import spark
from pyspark.sql import SparkSession


os.environ["SPARK_HOME"] = "/Users/lalithajetty/Downloads/spark-2.3.1-bin-hadoop2.7/"
os.environ["HADOOP_HOME"] = "/usr/local/Cellar/hadoop/3.1.0"
#os.environ["PYSPARK_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"
#os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"

data = spark.read.format("csv").option("header", "true").load("/Users/lalithajetty/PycharmProjects/Spark_ICP6/Immunotherapy.csv")

spark = SparkSession.builder.getOrCreate()

data = spark.read.load("immunotherapy.csv", format="csv", header=True, delimiter=",")
data = data.withColumn("AGE_FACTOR", data['age'] - 0).withColumn("Area", data['Area'] - 0).withColumn("I_D", data["induration_diameter"] - 0).withColumn("label", data['sex'] - 0)
data.show(100)
assem = VectorAssembler(inputCols=["AGE_FACTOR", "Area", "I_D"], outputCol='features')
data = assem.transform(data)


# Split the data into train and test
splits = data.randomSplit([0.8, 0.2], 1234)
train = splits[0]
test = splits[1]

# create the trainer and set its parameters
nb = NaiveBayes(smoothing=1.0, modelType="multinomial")

# train the model
model = nb.fit(train)

# select example rows to display.
predictions = model.transform(test)
predictions.show(100)

# compute accuracy on the test set
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                              metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test set accuracy = " + str(accuracy))