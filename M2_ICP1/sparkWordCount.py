import os
from operator import add
from pyspark import SparkContext

os.environ["SPARK_HOME"] = "/Users/lalithajetty/Downloads/spark-2.3.1-bin-hadoop2.7/"
os.environ["HADOOP_HOME"] = "/usr/local/Cellar/hadoop/3.1.0"
os.environ["PYSPARK_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"


if __name__ == "__main__":
    sc = SparkContext.getOrCreate()
    #sc.setLogLevel(1)

    lines = sc.textFile('sample.txt', 1)

    counts = lines.flatMap(lambda x: x.split(' ')) \
        .map(lambda x: (x, 1))\
        .reduceByKey(add)

    counts.saveAsTextFile("output.txt")
    sc.stop()

