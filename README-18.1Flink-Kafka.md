# 18. Using Event Time Temporal Joins and Lookup Joins to Enrich Ride Data: Hands On (2_flink_table_data)

## 0 Java 11 (WSL)

cd ~
rm FlinkData -r
mkdir FlinkData
cd FlinkData/
mkdir Rides
cd ..

nano .bashrc
    export KAFKA_HOME=~/kafka/kafka_2.12-3.5.2
    export JAVA_HOME=/usr
    export FLINK_HOME=~/flink/flink-1.17.2
    export PATH=$PATH:$FLINK_HOME/bin:$KAFKA_HOME/bin

source ~/.bashrc
echo $JAVA_HOME
    /usr

java --version
    openjdk 11.0.22 2024-01-16
    OpenJDK Runtime Environment (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1)
    OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1, mixed mode, sharing)

echo $KAFKA_HOME
    /home/christseng/kafka/kafka_2.12-3.5.2

kafka-topics.sh --version
    3.5.2

echo $FLINK_HOME
    /home/christseng/flink/flink-1.17.2

flink --version
    Version: 1.17.2, Commit ID: c0027e5

### 1 Start Flink Server

start-cluster.sh
    Starting cluster.
    Starting standalonesession daemon on host Chris-SP8.
    Starting taskexecutor daemon on host Chris-SP8.

<http://localhost:8081>

tail -f $FLINK_HOME/log/flink-*-taskexecutor-*.out

### 1.1 Test Flink Examples (Optional)

flink run $FLINK_HOME/examples/streaming/WordCount.jar
flink run $FLINK_HOME/examples/streaming/TopSpeedWindowing.jar

// Test Socket Port 9000
nc -lk 9000
nc -zv localhost 9000
    Connection to localhost (127.0.0.1) 9000 port [tcp/*] succeeded!

flink run $FLINK_HOME/examples/streaming/SocketWindowWordCount.jar --port 9000
    Starting Socket Window WordCount
    Use nc -lk 9000 to send data to the socket

// nc input
    Hello World
    Test 123

### 1.2 Flink Log

    (nymph,1)
    (in,3)
    (thy,1)
    (orisons,1)
    (be,4)
    ...

    (1,55,8591.666666666666,1715942690283)
    (1,55,8591.666666666666,1715942690283)
    (1,55,8591.666666666666,1715942690283)
    ...

    Hello : 1
    World : 1
    Test : 1
    123 : 1

## 2 Start Kafka Server

KAFKA_CLUSTER_ID="$($KAFKA_HOME/bin/kafka-storage.sh random-uuid)"
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c $KAFKA_HOME/config/kraft/server.properties
    Formatting /tmp/kraft-combined-logs with metadata.version 3.5-IV2.
kafka-server-start.sh -daemon $KAFKA_HOME/config/kraft/server.properties
ps -ef | grep kafka

### 2.1 Delete the consumer topics and groups (Optional)

kafka-topics.sh --bootstrap-server [::1]:9092 --list
// If exist then delete all topics

kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic rides
kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic riders
kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic drivers
kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic rides_enriched

### 2.2 Create the consumer topics and group 'rides-flink-consumer'

kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic riders
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic drivers
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides_enriched
kafka-topics.sh --bootstrap-server [::1]:9092 --list
    drivers
    riders
    rides
    rides_enriched

### 3 Input Data (2_flink_table_data) for Riders -> Drivers -> Rides

// Test flink run ...
flink run -c org.example.TestRideExample target/realtime-analytics-example-1.0-SNAPSHOT.jar
    RideTest table created
    Query RideTest table...
    Job has been submitted with JobID 92afb06a98b6853a6b9c8a0d53870c3f

// Flink run real data (riders, drivers, rides)...
flink run -c org.example.RideEnrichExample target/realtime-analytics-example-1.0-SNAPSHOT.jar

kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic drivers
kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic riders
kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic rides

### 4 Run the RideEnrichExample from the IDE then Query the rides_enriched topic again (not working)

kafka-console-consumer.sh --bootstrap-server [::1]:9092 --property print.key=true --topic rides_enriched
// Not working ...

<https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/kafka/>
<https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/upsert-kafka/>
<https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sql/queries/joins/#temporal-joins>
