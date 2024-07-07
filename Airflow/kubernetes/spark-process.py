from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark_conn = (SparkSession.builder.appName("Spark Processing").getOrCreate())

    print("Spark Session created")
    print("Hello World!")
    
    spark_conn.stop()
    