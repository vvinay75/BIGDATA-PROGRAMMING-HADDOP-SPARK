from pyspark import SparkConf, SparkContext, StorageLevel
import sys
import os

os.environ["SPARK_HOME"] = "/Users/lalithajetty/Downloads/spark-2.3.1-bin-hadoop2.7/"
os.environ["HADOOP_HOME"] = "/usr/local/Cellar/hadoop/3.1.0"
os.environ["PYSPARK_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/Cellar/python/3.6.5_1/bin/python3.6"

APP_NAME = "TwoPhaseMatrixMultiplication"

# Generate multiply elements in two matrixes
def mul(elements):  # elements = (key1, [('A',i, value)...('B',j, value)...)])

    _ma = list()
    _mb = list()
    _result = list()
    for _lst in elements[1]:  # element[1]=[('A',i, value)...('B',j, value)...)]
        if str(_lst[0]) == "A":
            _ma.append([str(_lst[1]), str(_lst[2])])
        else:
            _mb.append([str(_lst[1]), str(_lst[2])])

    for _elA in _ma:  # [[idx1, v1],[idx2, v2]]
        for _elB in _mb:
            _result.append(((str(_elA[0]), str(_elB[0])), int(_elA[1]) * int(_elB[1])))
    #if DEBUG: print('_result=%s' % (str(_result)))
    return _result  # ((i,j), multiplication)


# Create a configuration for this job
conf = SparkConf().setAppName(APP_NAME)

# Create a context for the job.
sc = SparkContext(conf=conf)

# creating RDD from external file for Matrix A and B.
rddALines = sc.textFile("M")  # ["0,0,A[0,0]", ..., "i, j, A[i,k]"]
rddBLines = sc.textFile("N")  # ["0,0,B[0,0]", ..., "k, j, B[k,j]"]


rddPhaseOneMapperA = rddALines.map(lambda x: x.split(',')).map(lambda data: (data[1], ['A', data[0], data[2]]))
rddPhaseOneMapperB = rddBLines.map(lambda x: x.split(',')).map(lambda data: (data[0], ['B', data[1], data[2]]))
rddPhaseOneMapperResult = rddPhaseOneMapperA.union(rddPhaseOneMapperB).groupByKey().map(lambda x: (x[0], list(x[1])))
rddPhaseOneReducer = rddPhaseOneMapperResult.flatMap(lambda e: mul(e)).persist(StorageLevel.MEMORY_ONLY_SER)
rddPhaseTwoMapper = rddPhaseOneReducer.map(lambda x: x)
rddPhaseTwoReducer = rddPhaseTwoMapper.reduceByKey(lambda x, y: x + y)
rddPhaseTwoReducerResult = rddPhaseTwoReducer.collect()


# print the results
for _x in rddPhaseTwoReducerResult:
    print("%s,%s\t%d" % (_x[0][0], _x[0][1], _x[1]))