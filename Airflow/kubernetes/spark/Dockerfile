# FROM bitnami/spark:3.5.1

# WORKDIR /opt/bitnami/spark
# COPY spark-process.py .
# Use the Apache Spark base image
FROM apache/spark:latest

# Set the working directory
WORKDIR /opt/spark

# Copy the Spark process script into the container
COPY spark-process.py .

# Update the package list and install Python3 and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean
RUN pip3 install --no-cache-dir pyspark

# Run the spark-process.py when the container starts
USER spark

ENV PYSPARK_PYTHON=python3
ENV PYTHONHASHSEED=1

CMD ["python3", "/opt/spark/spark-process.py"]
