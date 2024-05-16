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

bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --delete --group rides-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --delete --group drivers-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --delete --group riders-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --delete --group rides_enriched-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --list

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

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides --group rides-flink-consumer
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic riders --group riders-flink-consumer
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic drivers --group drivers-flink-consumer
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --group rides_enriched-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::]:9092 --list
    rides-flink-consumer
    riders-flink-consumer
    drivers-flink-consumer
    rides_enriched-flink-consumer

bin/kafka-consumer-groups.sh --bootstrap-server [::1]:9092 --describe --group rides-flink-consumer
    GROUP                TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID  
    rides-flink-consumer rides           0          0               0               0               -               -
    rides-flink-consumer rides           1          0               0               0               -               -
    rides-flink-consumer rides           2          0               0               0               -               -

bin/kafka-consumer-groups.sh --bootstrap-server [::1]:9092 --describe --group riders-flink-consumer
bin/kafka-consumer-groups.sh --bootstrap-server [::1]:9092 --describe --group drivers-flink-consumer
// ???
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic drivers --group testGroup

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic riders --group testGroup

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --group testGroup

bin/kafka-consumer-groups.sh --bootstrap-server [::1]:9092 --describe --group testGrou
    GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
    testGroup       drivers         1          2               2               0
    testGroup       riders          1          1               1               0
    testGroup       rides_enriched  1          0               0               0

### ??3 Test Query Kafka Topics 'rides' then 2.1 and 2.2 again

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides --group rides-flink-consumer

cd $KAFKA_HOME
bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

{ "ride_id":"000001"}@@@{"ride_id": "000001","rider_id": "100001","driver_id": "200001","location_id": "300001","amount": 350,"ride_status": "Booked","start_lat" : 12.990707,"start_lng" : 77.570870,"dest_lat": 12.887725, "dest_lng": 77.560973}

### 4 First Run the RideEnrichExample in IntelliJ 

// bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --property print.key=true

// IntelliJ - Run the RideEnrichExample

### 5 Input Data (2_flink_table_data) for Riders -> Drivers -> Rides

bin/kafka-console-producer.sh --topic riders --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

bin/kafka-console-producer.sh --topic drivers --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

// Run the RideEnrichExample from the IDE 

### 7 Query the rides_enriched topic again (not working)

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --property print.key=true
