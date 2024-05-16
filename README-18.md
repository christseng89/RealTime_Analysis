# 18. Using Event Time Temporal Joins and Lookup Joins to Enrich Ride Data: Hands On (2_flink_table_data)

## 0 Java 11 (WSL)

cd ~
rm FlinkData -r
mkdir FlinkData
cd FlinkData/
mkdir Rides
cd ..

source ~/.bashrc
echo $JAVA_HOME
    /usr

java --version
    openjdk 11.0.22 2024-01-16
    OpenJDK Runtime Environment (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1)
    OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1, mixed mode, sharing)

echo $KAFKA_HOME
    /home/christseng/kafka/kafka_2.12-3.5.2

$KAFKA_HOME/bin/kafka-topics.sh --version
    3.5.2

echo $FLINK_HOME
    /home/christseng/flink/flink-1.17.2

flink --version
    Version: 1.17.2, Commit ID: c0027e5

### 1 Start Flink Server

$FLINK_HOME/bin/start-cluster.sh
    Starting cluster.
    Starting standalonesession daemon on host Chris-SP8.
    Starting taskexecutor daemon on host Chris-SP8.

$FLINK_HOME/bin/sql-client.sh
ps aux | grep flink
    christs+  586603 50.0 23.6 9174280 2900328 ?     Ssl  17:21  15:33 /usr/bin/java --add-opens java.base/java.lang=ALL-UNNAMED -Dfile.encoding=UTF-8 -classpath /mnt/d/development/Real_Time_Analysis/realtime_analysis/target/classes:/

flink run $FLINK_HOME/examples/streaming/WordCount.jar
tail $FLINK_HOME/log/flink-*-taskexecutor-*.out
    (nymph,1)
    (in,3)
    (thy,1)
    (orisons,1)
    (be,4)
    (all,2)
    (my,1)

<http://localhost:8081>

## 2 Start Kafka Server

cd $KAFKA_HOME
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
    Formatting /tmp/kraft-combined-logs with metadata.version 3.5-IV2.
bin/kafka-server-start.sh -daemon config/kraft/server.properties
ps -ef | grep kafka

### 2.1 Delete the consumer topics and groups (Rerun)

bin/kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic rides
bin/kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic riders
bin/kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic drivers
bin/kafka-topics.sh --delete --bootstrap-server [::1]:9092 --topic rides_enriched
bin/kafka-topics.sh --bootstrap-server [::1]:9092 --list

### 2.2 Create the consumer topics and group 'rides-flink-consumer'

bin/kafka-topics.sh --create --topic rides --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic riders --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic drivers --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic rides_enriched --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 
bin/kafka-topics.sh --bootstrap-server [::1]:9092 --list
    drivers
    riders
    rides
    rides_enriched

### 3 Input Data (2_flink_table_data) for Riders -> Drivers -> Rides

bin/kafka-console-producer.sh --topic riders --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

bin/kafka-console-producer.sh --topic drivers --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

### 4 Run the RideEnrichExample from the IDE then Query the rides_enriched topic again (not working)

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --property print.key=true
// Not working ...

<https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/kafka/>
<https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/upsert-kafka/>
